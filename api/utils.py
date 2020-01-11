import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from os.path import basename


class Sender:

    def __init__(self, email, password):
        host = "smtp.gmail.com"
        port = 587
        self.email = email
        sender = smtplib.SMTP(host=host, port=port)
        sender.starttls()
        sender.login(email, password)
        self.s = sender
        msg = MIMEMultipart()
        self.msg = msg
        self.msg['To'] = email

    def add_attachments(self, path):
        with open(path, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(path)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(path)
        self.msg.attach(part)

    def add_body(self, body):
        self.msg.attach(MIMEText(body, "plain"))

    def add_recipient(self, email):
        self.msg['To'] = email

    def add_subject(self, subject):
        self.msg['subject'] = subject

    def send(self):
        self.s.send_message(self.msg)
        del self.msg
        self.s.quit()
