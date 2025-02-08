import json
import requests
import time
import smtplib
import logging
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pytz  # Timezone conversion
from email_helper import generate_alert_email_body, generate_resolved_email_body

# Load Configuration
def load_config():
    """Loads configuration from config.json"""
    try:
        with open("config.json", "r") as file:
            config = json.load(file)
        logging.info("✅ Config loaded successfully.")
        return config
    except Exception as e:
        logging.critical(f"🚨 Failed to load config.json: {e}")
        exit(1)

config = load_config()

# Constants from Config
PSN_API_URL     = config["PSN_API_URL"]
SMTP_SERVER     = config["SMTP_SERVER"]
SMTP_PORT       = config["SMTP_PORT"]
EMAIL_SENDER    = config["EMAIL_SENDER"]
EMAIL_PASSWORD  = config["EMAIL_PASSWORD"]
EMAIL_RECEIVER  = config["EMAIL_RECEIVER"]
RETRY_DELAY     = config["RETRY_DELAY"]
MAX_RETRIES     = config["MAX_RETRIES"]
CHECK_INTERVAL  = config["CHECK_INTERVAL"]

# Logging Configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("psn_monitor.log"),
        logging.StreamHandler()
    ]
)
logging.getLogger().setLevel(logging.DEBUG)
logging.info("✅ Logging enabled: Writing to both file & console.")

# Timezones
IST = pytz.timezone("Asia/Kolkata")
UTC = pytz.utc

def format_time(iso_time):
    """Converts ISO 8601 time to human-readable IST and UTC format."""
    try:
        dt_utc = datetime.strptime(iso_time, "%Y-%m-%dT%H:%M:%S.%f%z")
        dt_ist = dt_utc.astimezone(IST)
        return dt_utc.strftime("%Y-%m-%d %H:%M:%S %Z"), dt_ist.strftime("%Y-%m-%d %I:%M %p %Z")
    except Exception as e:
        logging.error(f"⏳ Time conversion error: {e}")
        return "Unknown", "Unknown"

def fetch_psn_status():
    """Fetches the latest PlayStation Network (PSN) status data."""
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(PSN_API_URL, timeout=10)
            logging.info(f"HTTP Status Code: {response.status_code}")
            if response.status_code != 200:
                logging.error(f"⚠️ Failed to fetch data. Status Code: {response.status_code}")
                retries += 1
                time.sleep(RETRY_DELAY)
                continue
            return response.json()
        except requests.RequestException as e:
            logging.error(f"🔥 Network error: {e}")
            retries += 1
            time.sleep(RETRY_DELAY)
    logging.error("❌ Failed to fetch PSN data after multiple attempts.")
    return None

def check_psn_status(data):
    """
    Parses PSN JSON data and extracts outage information.
    Filters for the country specified in config.json.
    """
    if not data or "countries" not in data:
        logging.warning("⚠️ No PSN data received or missing 'countries' key.")
        return []

    logging.info("🔍 Checking PSN status for outages...")

    outages = []
    target_country = config.get("CountryName", "India")  # Fetch from config

    for country in data["countries"]:
        country_name = country.get("countryName", "Unknown")

        # Filter only for the target country (India)
        if country_name.lower() != target_country.lower():
            continue  # Skip other countries

        logging.info(f"🔎 Checking outages for {country_name}")

        for status in country.get("status", []):
            if status.get("statusType", "").lower() == "outage":
                affected_devices = [device.get("deviceName", "Unknown Device") for device in status.get("devices", [])]
                message = status.get("message", {}).get("messages", {}).get("en-GB", "No message available")
                messageKey = status.get("message", {}).get("messageKey", {})
                start_time_utc, start_time_ist = format_time(status.get("startDate", "Unknown"))

                outage_info = {
                    "country": country_name,
                    "statusId": status.get("statusId", "Unknown"),
                    "startDateUTC": start_time_utc,
                    "startDateIST": start_time_ist,
                    "affectedDevices": affected_devices,
                    "affectedService": messageKey.split(".")[1] if messageKey else "",
                    "message": message
                }

                outages.append(outage_info)
                logging.warning(f"🚨 Outage Detected in {country_name}: {outage_info}")

    if outages:
        logging.info(f"⚠️ {len(outages)} outage(s) found in {target_country}!")
    else:
        logging.info(f"✅ No PSN outages detected in {target_country}.")

    return outages


def send_email_notification(subject, body):
    """
    Sends an email with the given subject and body.
    This function centralizes the email sending logic.
    """
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        logging.info(f"📧 Email with subject '{subject}' sent successfully.")
    except Exception as e:
        logging.error(f"🚨 Email sending failed: {e}")

def send_outage_email(outages):
    """Sends an outage notification email."""
    subject = "⚠️ PSN Service Outage Alert - Affected Devices & Status"
    email_body = generate_alert_email_body(outages)
    send_email_notification(subject, email_body)

def send_resolved_email():
    """Sends a resolved notification email when previously detected outages have cleared."""
    subject = "✅ PSN Service Resolved - All Systems Normal"
    email_body = generate_resolved_email_body()
    send_email_notification(subject, email_body)

def monitor_psn():
    """
    Monitors PlayStation Network status **every hour**.
    - Sends an alert **only if PSN goes down**.
    - Sends a resolved email **when PSN recovers**.
    - Avoids duplicate emails for the same issue.
    """
    logging.info("🔍 PSN Monitoring Started... Checking every hour.")
    outage_active = False  # Flag to track active outage

    while True:
        psn_data = fetch_psn_status()
        outage_reports = check_psn_status(psn_data)

        if outage_reports and not outage_active:
            send_outage_email(outage_reports)
            outage_active = True  # Mark outage as active

        elif not outage_reports and outage_active:
            send_resolved_email()
            outage_active = False  # Mark system as restored

        logging.info(f"🕒 Next check in {CHECK_INTERVAL} secs...")
        time.sleep(CHECK_INTERVAL)  # Wait for 1 hour before checking again

if __name__ == "__main__":
    monitor_psn()
