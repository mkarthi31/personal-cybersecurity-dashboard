# main.py
# Streamlit UI for demo dashboard.

import streamlit as st
from breach_checker import check_and_alert, init_db
from zxcvbn import zxcvbn  # optional

init_db()

st.set_page_config(page_title="Personal Cybersecurity Dashboard", layout="centered")
st.title("Personal Cybersecurity Dashboard (Demo)")

st.markdown("""
**Demo mode:** this project runs with mock breach data for testing.  
When you have API keys and SMTP credentials you can connect real services — see breach_checker.py comments.
""")

email = st.text_input("Enter your email to check breaches", placeholder="demo@example.com")
password = st.text_input("Check password strength", type="password")

if st.button("Check Breaches"):
    if email:
        res = check_and_alert(email, alert_if_empty=True)
        if res.get("new_alert"):
            st.warning("New Breaches Found:")
            for b in res.get("breaches", []):
                st.write("- " + b)
        else:
            st.success("No new breaches found (or already recorded).")

if st.button("Check Password"):
    if password:
        try:
            score = zxcvbn(password)['score']
            st.info(f"Password Strength Score: {score} / 4")
        except Exception:
            st.info("Password strength check unavailable (install zxcvbn-python).")
