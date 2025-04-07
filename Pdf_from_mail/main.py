import imaplib
import email
from email.header import decode_header
import os
import logging

#  Configuration
EMAIL = "demo@gmail.com"
APP_PASSWORD = "12345"  
IMAP_SERVER = "imap.gmail.com"
RESUME_FOLDER = "Resume"
SENDER_FILTER = None  

#  Setup Logging 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Create Resume Folder 
if not os.path.exists(RESUME_FOLDER):
    os.makedirs(RESUME_FOLDER)
    logging.info(f"Created folder: {RESUME_FOLDER}")

# Helper Function
def clean_filename(name):
    return "".join(c if c.isalnum() or c in " ._-" else "_" for c in name)

def connect_to_gmail():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, APP_PASSWORD)
        logging.info("Successfully connected to Gmail.")
        return mail
    except imaplib.IMAP4.error as e:
        logging.error(f"Login failed: {e}")
        exit(1)

def search_emails(mail):
    mail.select("inbox")
    criteria = '(UNSEEN)'
    if SENDER_FILTER:
        criteria = f'(OR UNSEEN FROM "{SENDER_FILTER}")'
    result, data = mail.search(None, criteria)
    if result != "OK":
        logging.warning("No emails found.")
        return []
    return data[0].split()

def download_attachments(mail, email_ids):
    downloaded_files = set()
    for eid in email_ids:
        result, data = mail.fetch(eid, "(RFC822)")
        if result != "OK":
            continue
        msg = email.message_from_bytes(data[0][1])
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()
            if filename and filename.lower().endswith(".pdf"):
                decoded_name, encoding = decode_header(filename)[0]
                if isinstance(decoded_name, bytes):
                    filename = decoded_name.decode(encoding or 'utf-8')
                filename = clean_filename(filename)
                filepath = os.path.join(RESUME_FOLDER, filename)
                if not os.path.exists(filepath):
                    with open(filepath, "wb") as f:
                        f.write(part.get_payload(decode=True))
                    downloaded_files.add(filename)
                    logging.info(f"Downloaded: {filename}")
                else:
                    logging.info(f"Skipped (already exists): {filename}")
       
        mail.store(eid, '+FLAGS', '\\Seen')

# Main 
def main():
    mail = connect_to_gmail()
    email_ids = search_emails(mail)
    if email_ids:
        logging.info(f"Found {len(email_ids)} matching emails.")
        download_attachments(mail, email_ids)
    else:
        logging.info("No matching emails found.")
    mail.logout()

if __name__ == "__main__":
    main()
