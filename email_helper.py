import datetime

def generate_alert_email_body(outages):
    """
    Generates an HTML email body for the PlayStation Network outage report
    using simple CSS and inline styles to enforce a dark background that is
    responsive on phones.

    Args:
        outages (list): List of dictionaries containing outage information

    Returns:
        str: HTML email content with simplified CSS for mobile compatibility
    """
    current_year = datetime.datetime.now().year

    # Build table rows for each outage
    table_rows = ""
    for outage in outages:
        table_rows += f"""
            <tr>
                <td style="border: 1px solid #333333; padding: 8px;"><strong>{outage['country']}</strong></td>
                <td style="border: 1px solid #333333; padding: 8px;">{outage['startDateIST']}</td>
                <td style="border: 1px solid #333333; padding: 8px;">{outage['affectedService']}</td>
                <td style="border: 1px solid #333333; padding: 8px;">{', '.join(outage['affectedDevices'])}</td>
                <td style="border: 1px solid #333333; padding: 8px; color: #D32F2F;">{outage['message']}</td>
            </tr>
        """

    # Build the full HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html style="background-color: #121212; margin: 0; padding: 0;">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>PSN Service Alert</title>
      <style type="text/css">
        /* Base styles */
        body {{
          background-color: #121212;
          color: #ffffff;
          font-family: Arial, sans-serif;
          margin: 0;
          padding: 0;
        }}
        .container {{
          background-color: #1E1E1E;
          margin: 20px auto;
          max-width: 800px;
          padding: 20px;
          border-radius: 8px;
        }}
        .alert-banner {{
          background-color: #D32F2F;
          text-align: center;
          padding: 10px;
          font-size: 22px;
          font-weight: bold;
        }}
        .content {{
          padding: 20px;
        }}
        table {{
          width: 100%;
          border-collapse: collapse;
          margin-top: 20px;
        }}
        th, td {{
          border: 1px solid #333333;
          padding: 8px;
          text-align: left;
        }}
        th {{
          background-color: #212121;
        }}
        tr:nth-child(even) {{
          background-color: #2C2C2C;
        }}
        tr:nth-child(odd) {{
          background-color: #1E1E1E;
        }}
        .footer {{
          background-color: #212121;
          text-align: center;
          padding: 20px;
          font-size: 14px;
          color: #B0B0B0;
          margin-top: 20px;
        }}
        a {{
          color: #D32F2F;
          text-decoration: none;
        }}
        a:hover {{
          text-decoration: underline;
        }}
        /* Responsive styles for phones */
        @media only screen and (max-width: 600px) {{
          .container {{
            margin: 10px auto;
            padding: 10px;
            width: 100% !important;
          }}
          .alert-banner {{
            font-size: 18px;
            padding: 8px;
          }}
          .content, .footer {{
            padding: 10px;
          }}
          table, th, td {{
            font-size: 14px;
          }}
        }}
      </style>
    </head>
    <body style="background-color: #121212; color: #ffffff; margin: 0; padding: 0;">
      <div class="container" style="background-color: #1E1E1E; margin: 20px auto; max-width: 800px; padding: 20px; border-radius: 8px;">
        <!-- Alert Banner -->
        <div class="alert-banner" style="background-color: #D32F2F; text-align: center; padding: 10px; font-size: 22px; font-weight: bold;">
          🚨 CRITICAL SERVICE ALERT 🚨
        </div>
        <!-- Main Content -->
        <div class="content" style="padding: 20px;">
          <p><strong>Dear PlayStation Network User,</strong></p>
          <p>We have detected <span style="color: #D32F2F;">critical service interruptions</span> affecting the PlayStation Network.</p>
          <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
            <thead>
              <tr>
                <th style="border: 1px solid #333333; padding: 8px; background-color: #212121;">Region</th>
                <th style="border: 1px solid #333333; padding: 8px; background-color: #212121;">Start Time (IST)</th>
                <th style="border: 1px solid #333333; padding: 8px; background-color: #212121;">Affected Service</th>
                <th style="border: 1px solid #333333; padding: 8px; background-color: #212121;">Affected Devices</th>
                <th style="border: 1px solid #333333; padding: 8px; background-color: #212121;">Status</th>
              </tr>
            </thead>
            <tbody>
              {table_rows}
            </tbody>
          </table>
          <p style="margin-top: 20px;"><strong>Impact:</strong> Users may experience difficulties accessing online services, gaming features, and digital content.</p>
          <p><strong>Next Steps:</strong> No action is required from your end. We will notify you once services are restored.</p>
        </div>
        <!-- Footer -->
        <div class="footer" style="background-color: #212121; text-align: center; padding: 20px; font-size: 14px; color: #B0B0B0; margin-top: 20px;">
          <p>© {current_year} Sony Interactive Entertainment Inc. All rights reserved.</p>
          <p style="margin-top: 8px;">This is an automated alert. Please do not reply to this email.</p>
          <p style="margin-top: 8px;">For real-time status updates, visit <a href="https://status.playstation.com">status.playstation.com</a></p>
        </div>
      </div>
    </body>
    </html>
    """
    return html_content



def generate_resolved_email_body():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>PSN Service Resolved</title>
    </head>
    <body style="background-color: #121212; color: #ffffff; font-family: Arial, sans-serif; padding: 20px;">
      <div style="max-width: 800px; margin: auto; padding: 20px;">
        <h1 style="color: #4CAF50;">PSN Service Resolved</h1>
        <p>Dear PlayStation Network User,</p>
        <p>The previously detected service interruptions have now been resolved and all systems are functioning normally.</p>
        <p>Thank you for your patience.</p>
        <p>Regards,<br/>PSN Status Monitor</p>
      </div>
    </body>
    </html>
    """