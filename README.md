# 🎮 PSN Monitoring Service 🚀

## 📌 Overview
This is a **PlayStation Network (PSN) Monitoring Service** that:
- **Fetches live PSN outage data** from the PlayStation API
- **Detects service disruptions** and affected devices
- **Sends email alerts** using SMTP when an outage is detected
- **Runs as a background systemd service** on Linux
- **Stores logs for debugging and analysis**

---

## 🛠️ **Installation & Setup**

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/sachdev27/psn-monitor.git
cd psn-monitor
```

### **2️⃣ Setup Virtual Environment & Install Dependencies**
```bash
chmod +x setup_and_run.sh
./setup_and_run.sh
```

This script will:
- **Create a Python Virtual Environment** (`venv/`)
- **Install dependencies** from `requirements.txt`
- **Setup and start the PSN monitoring service**

---

## ⚙️ **Configuration**

Edit the **config.json** file to update email credentials and API settings:
```json
{
  "psn_api_url": "https://status.playstation.com/data/statuses/region/SCEE.json",
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "email_sender": "your_email@gmail.com",
  "email_password": "your_app_password",
  "email_receiver": "receiver_email@example.com",
  "retry_delay": 10,
  "max_retries": 5,
  "check_interval": 3600
}
```
🔹 **email_password** → Use a [Google App Password](https://myaccount.google.com/apppasswords)
🔹 **check_interval** → Set time interval (in seconds) for checking PSN status

---

## 🚀 **Running the Service as a Background Process**
This project runs **as a systemd service** on Linux.

### **1️⃣ Check Service Status**
```bash
sudo systemctl status psn_monitor
```

### **2️⃣ Restart the Service**
```bash
sudo systemctl restart psn_monitor
```

### **3️⃣ Stop the Service**
```bash
sudo systemctl stop psn_monitor
```

### **4️⃣ Enable Service on Startup**
```bash
sudo systemctl enable psn_monitor
```

---

## 📧 **Email Alerts**
- Sends **beautiful HTML email notifications** when a PSN outage occurs.
- Uses a **dark-themed PlayStation OG design**.
- Includes **affected regions, devices, and downtime details**.

✅ **Example Email Alert:**
Email Screenshot   <img width="1416" alt="image" src="https://github.com/user-attachments/assets/d47d60b8-469f-46e5-87cc-f4bc891aa1f6" />


---

## 📜 **Logging & Debugging**
All logs are stored in `psn_monitor.log`.

### **View Logs in Real-Time:**
```bash
tail -f psn_monitor.log
```

### **Example Log Output**
```
2025-02-08 12:00:00 INFO ✅ Logging enabled: Writing to both file & console.
2025-02-08 12:01:10 WARNING 🚨 PSN Outage Detected! Sending email alert...
2025-02-08 12:02:00 INFO ✅ Email sent successfully.
```

---

## 📢 **Contributing**
Contributions are welcome! To contribute:
1. **Fork** the repository
2. **Create a new branch** (`git checkout -b feature-branch`)
3. **Commit changes** (`git commit -m "Added new feature"`)
4. **Push to GitHub** (`git push origin feature-branch`)
5. **Open a Pull Request**

---

## 📄 **License**
This project is **open-source** and licensed under the **MIT License**.

---

## ❤️ **Support**
If you find this project useful, **star ⭐ the repo** and spread the word!
Have questions? Open an **issue** or reach out.

---
