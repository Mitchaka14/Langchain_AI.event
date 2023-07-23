import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import streamlit as st
from dotenv import load_dotenv

try:
    p = st.secrets["CodedP"]
except Exception:
    load_dotenv()
    p = os.getenv("CodedP")


def send_email(subject, content):
    # Extract email address from the content string
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    match = re.search(email_pattern, content)

    if not match:
        return "No email address detected in the content"

    user_email = match.group()
    message = content.replace(user_email, "")  # Remove email from the message

    # create message object instance
    msg = MIMEMultipart()

    # setup the parameters of the message
    password = p
    msg["From"] = "voiceverseverse@gmail.com"
    msg["To"] = user_email
    msg["Subject"] = subject

    # add in the message body
    msg.attach(MIMEText(message, "plain"))

    # create server
    server = smtplib.SMTP("smtp.gmail.com", 587)

    # starting the server instance
    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg["From"], password)

    # send the message via the server
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()

    return f"Email successfully sent to {user_email}"


# using the function
subject = "Hello"
content = (
    "This is a test email. Regards, mitchel. this was sent to akaelumitchell@gmail.com"
)
print(send_email(subject, content))
