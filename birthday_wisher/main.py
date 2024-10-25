import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def send_wish(sender_email, receiver_email, Appassword, body, subject, address):
    # Create the message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = address
    message["Subject"] = subject

    # Email body
    message.attach(MIMEText(body, "plain"))

    # Setup the server connection using Gmail's SMTP
    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Secure the connection using TLS
        server.login(sender_email, Appassword)  # Login to your email account

        # Send the email
        server.sendmail(sender_email, address, message.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

    finally:
        # Close the server connection
        server.quit()


def retrieve_from_sheet():

    try:
        url = os.getenv("API_URL")

        response = requests.get(url)
        data = response.json()

        return data["sheet1"]

    except Exception as e:
        print("Could not fetch data: {e}")


def write_birthday_msg():
    data = retrieve_from_sheet()

    today = datetime.now().strftime("%d %B")  # Get current date in "MM-DD" format
    this_year = datetime.now().year

    # print(this_year)
    # print(today)

    def get_ordinal_suffix(day):
        if 10 <= day % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        return suffix

    for i in data:

        birthday_date = datetime.strptime(i["birthday"], "%d %B %Y").strftime("%d %B")
        birth_year = datetime.strptime(i["birthday"], "%d %B %Y").year

        if birthday_date == today:

            age = this_year - birth_year
            suffix = get_ordinal_suffix(age)
            email_address = i["email"]
            birthday_subject = f"Birthday wishes {i['name']}"
            birthday_message = f"Happy {age}{suffix} Birthday to you {i['name']}. wish you  a very special day. have a wonderful day dear\n\n kind regards:\n Aloy@Wethinkcode"
            return birthday_message, birthday_subject, email_address


message, subject, address = write_birthday_msg()
# Email configuration
sender_email = os.getenv("EMAIL_USER")
receiver_email = "sathekgealoy@gmail.com"
APP_PASSWORD = os.getenv("EMAIL_PASSWORD")
send_wish(sender_email, address, APP_PASSWORD, message, subject, address)
