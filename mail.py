import smtplib, os
from dotenv import find_dotenv, load_dotenv

ENV = find_dotenv()
load_dotenv(ENV)

class SendEmail:
    def __init__(self, message):
        self.message = message
        self.mail()

    def mail(self):
        # Sending Email<
        fromMail = os.getenv("FROM")
        password = os.getenv("PASSWORD")
        toMail =  os.getenv("TO")

        # Security
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            # Login
            smtp.login(fromMail, password)

            # Content of Message
            subject = "Reminder"
            body = self.message

            # Single Message
            msg = f"subject:{subject}\n\n{body}"

            # Send Mail
            smtp.sendmail(fromMail, toMail, msg)