import imaplib
import email
from email.header import decode_header
from typing import List, Dict

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

def connect_imap(username: str, password: str):
    if not username or not password:
        raise ConnectionError("Email and password are required for IMAP login.")
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(username, password)
        return mail
    except Exception as e:
        raise ConnectionError(f"IMAP connection failed: {e}")

def fetch_support_emails(mail, mailbox="INBOX") -> List[Dict]:
    try:
        mail.select(mailbox)
        status, messages = mail.search(None, 'ALL')
        email_ids = messages[0].split()
        filtered_emails = []
        for eid in email_ids:
            status, msg_data = mail.fetch(eid, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    try:
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else "utf-8")
                        sender = msg.get("From")
                        date = msg.get("Date")
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode(errors="ignore")
                                    break
                        else:
                            body = msg.get_payload(decode=True).decode(errors="ignore")
                        filtered_emails.append({
                            "sender": sender,
                            "subject": subject,
                            "body": body,
                            "date": date
                        })
                    except Exception as e:
                        continue
        return filtered_emails
    except Exception as e:
        import traceback
        print("Email fetching failed:", traceback.format_exc())
        raise RuntimeError(f"Email fetching failed: {e}")