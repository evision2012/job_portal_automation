import pandas as pd
import smtplib
from email.mime.text import MIMEText
import re

# --- CONFIGURATION ---
EXCEL_FILE = "sample_student_data.xlsx"
SENDER_EMAIL = "rishukanha78@gmail.com"
APP_PASSWORD = "ypmddeujmvwcqmsf"

SIMULATE = True 

# --- GET FILTER INPUT FROM USER ---
try:
    min_exp = int(input("Enter minimum experience (in years): "))
    max_exp = int(input("Enter maximum experience (in years): "))
    min_grad_year = int(input("Enter earliest graduation year: "))
    max_grad_year = int(input("Enter latest graduation year: "))
except Exception as e:
    print("Invalid input. Please enter numeric values only.")
    exit()

# --- EMAIL CONTENTS ---
def get_email_content(name, shortlisted=True):
    if shortlisted:
        return f"""Dear {name},

Congratulations! Based on your profile, you have been shortlisted for the next round.

Best regards,
HR Team"""
    else:
        return f"""Dear {name},

Thank you for applying. Unfortunately, you have not been shortlisted at this stage.

We wish you all the best in your future endeavors.

Warm regards,
HR Team"""

# --- FUNCTION TO SEND EMAIL OR SIMULATE ---
def send_email(receiver_email, name, shortlisted=True):
    body = get_email_content(name, shortlisted)
    msg = MIMEText(body, "plain")
    msg["Subject"] = "Application Status"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    if SIMULATE:
        print(f"📧 Email to {name} ({receiver_email}) - {'Shortlisted' if shortlisted else 'Not Shortlisted'}")
        return

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        print(f"✅ Email sent to {name} ({'Shortlisted' if shortlisted else 'Not Shortlisted'})")
    except Exception as e:
        print(f"❌ Failed to send email to {name}: {e}")

# --- MAIN EXECUTION ---
def main():
    try:
        df = pd.read_excel(EXCEL_FILE)
    except Exception as e:
        print(f"Failed to read Excel file: {e}")
        return

    for index, row in df.iterrows():
        name = str(row.get("Name", "")).strip()
        email = str(row.get("Email ID", "")).strip()
        experience_text = str(row.get("Total Experience", "")).lower().strip()
        graduation_year = str(row.get("UG Graduation year", "0")).strip()

        # Parse experience
        if "fresher" in experience_text or experience_text in ["na", "", "nan"]:
            exp_years = 0
        else:
            try:
                exp_years = int(re.search(r'\d+', experience_text).group())
            except:
                exp_years = 0

        # Parse graduation year
        try:
            grad_year = int(re.search(r'\d{4}', graduation_year).group())
        except:
            grad_year = 0

        # Debug print
        print(f"{name} → Experience: {exp_years} years, Graduation Year: {grad_year}")

        # Apply filters
        shortlisted = (min_exp <= exp_years <= max_exp) and (min_grad_year <= grad_year <= max_grad_year)

        # Send or simulate email
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            send_email(email, name, shortlisted)
        else:
            print(f"⚠️ Invalid email for {name}: {email}")

# Run the script
if __name__ == "__main__":
    main()
