import smtplib

class SendEmail:
    def __init__(self, message):
        self.message = message
        self.mail()

    def mail(self):
        # Sending Email<
        mail = "hhubele890@gmail.com"
        password = "hhu19989898"

        # Security
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            # Login
            smtp.login(mail, password)

            # Content of Message
            subject = "Reminder"
            body = self.message

            # Single Message
            msg = f"subject:{subject}\n\n{body}"

            # Send Mail
            smtp.sendmail(mail, "muhammedakbulut98@std.sehir.edu.tr", msg)