✉️ Simple Email Script with smtplib using Gmail App Password

import smtplib
from email.mime.text import MIMEText

# Email details
sender = "sender_email@gmail.com"
receiver = "receiver_email@gmail.com"
password = "your_app_password"  # Use Gmail App Password

msg = "Hello, World! What's up"

# Email content
message = MIMEText(msg, "plain")
message["Subject"] = "Test Email"
message["From"] = sender
message["To"] = receiver

# Send the email using Gmail's SMTP server
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(message)
    print("Email sent successfully.")
except Exception as e:
    print("Failed to send email:", e)


