# breach_checker.py
# Check emails for breaches, record them to SQLite, and send alerts.
# Default mode: will send real emails if email_config.py is filled and real_smtp=True.
# For safety, by default this file will fall back to printing simulated emails
# if email_config.py doesn't provide valid credentials or if real_smtp is False.

import sqlite3
from datetime import datetime
from fake_breaches import fake_breaches

# optional import for real SMTP; email_config.py should contain credentials
try:
    from email_config import EMAIL_ADDRESS, EMAIL_PASSWORD
except Exception:
    EMAIL_ADDRESS = None
    EMAIL_PASSWORD = None

DB_PATH = "db.sqlite"

def _get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    # create tables if they don't exist
    conn = _get_conn()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS breaches (
                    email TEXT,
                    breach_name TEXT,
                    date TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS alerts (
                    email TEXT,
                    reason TEXT,
                    ts TEXT
                )''')
    conn.commit()
    conn.close()

# --------------------------
# Email sending - two modes
# --------------------------
# real_smtp = True  -> tries to send via SMTP using values from email_config.py
# real_smtp = False -> prints simulated email to console (safe default)
#
# WARNING: If you enable real_smtp make sure you use an App Password (Gmail).
# DO NOT commit email_config.py to source control.
real_smtp = True  # set to False if you want to avoid sending real emails while testing

def _send_via_smtp(recipient, subject, body):
    # Import inside function to avoid import error if smtplib not available
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise RuntimeError("EMAIL_ADDRESS or EMAIL_PASSWORD not set in email_config.py")

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()

def send_email(recipient, subject, body):
    """
    Sends an email if real_smtp is True and credentials exist.
    Otherwise prints a simulated email to the console.
    """
    if real_smtp and EMAIL_ADDRESS and EMAIL_PASSWORD:
        try:
            _send_via_smtp(recipient, subject, body)
            print(f"[Email] Sent real email to {recipient}")
        except Exception as e:
            # fallback to simulated output on failure
            print(f"[Email] Failed to send real email ({e}). Falling back to simulated print.")
            _print_simulated_email(recipient, subject, body)
    else:
        _print_simulated_email(recipient, subject, body)

def _print_simulated_email(recipient, subject, body):
    print(f"\n--- Simulated Email to {recipient} ---")
    print(f"Subject: {subject}")
    print(body)
    print("--- End Simulated Email ---\n")

# --------------------------
# Breach checking (mock)
# --------------------------
def check_breach(email):
    """
    Mock-mode check: looks up email in fake_breaches dict.
    Inserts any new breach entries into the DB and returns a list of new breaches.
    """
    conn = _get_conn()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS breaches (
                    email TEXT,
                    breach_name TEXT,
                    date TEXT
                )''')
    conn.commit()

    breaches = fake_breaches.get(email, [])
    new_breaches = []

    for b in breaches:
        name = b.get('Name')
        date = b.get('BreachDate')
        c.execute("SELECT 1 FROM breaches WHERE email=? AND breach_name=?", (email, name))
        if not c.fetchone():
            c.execute("INSERT INTO breaches VALUES (?, ?, ?)", (email, name, date))
            new_breaches.append(f"{name} on {date}")

    conn.commit()
    conn.close()
    return new_breaches

def check_and_alert(email, alert_if_empty=False):
    """
    High-level helper called by UI and scheduler.
    Checks for new breaches, records alert history and sends email (real or simulated).
    """
    new_breaches = check_breach(email)
    if new_breaches:
        body = f"New breaches detected for {email}:\n\n" + "\n".join(new_breaches)
        send_email(email, "Cybersecurity Alert", body)
        # record alert to DB
        conn = _get_conn()
        c = conn.cursor()
        c.execute("INSERT INTO alerts VALUES (?, ?, ?)", (email, "; ".join(new_breaches), datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
        return {"new_alert": True, "breaches": new_breaches}
    else:
        if alert_if_empty:
            send_email(email, "Cybersecurity Check", f"No new breaches detected for {email}.")
        return {"new_alert": False, "breaches": []}

# initialize DB on import
init_db()
