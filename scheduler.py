# scheduler.py
# Run this to enable periodic checks. For quick testing, the schedule can be changed to run every minute.

import schedule
import time
from breach_checker import check_and_alert

# add the emails you want the scheduler to monitor
emails_to_monitor = [
    "m.karthigan31@gmail.com",   # your test email
    "demo@example.com",
    "multi_leaks@example.com"
]

def job():
    print(f"[Scheduler] Running check at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    for email in emails_to_monitor:
        res = check_and_alert(email)
        if res.get("new_alert"):
            print(f"[{email}] New alert recorded (email sent/simulated).")
        else:
            print(f"[{email}] No new breaches.")

# default schedule: every day at 09:00
schedule.every().day.at("09:00").do(job)

# For testing you can uncomment the following line to run every minute:
schedule.every(1).minutes.do(job)

print("Scheduler started. Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(30)
