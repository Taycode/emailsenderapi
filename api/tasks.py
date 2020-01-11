import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from os.path import basename
from celery import shared_task


@shared_task
def sender_func(email, password, recipient, subject, body, path):
    host = "smtp.gmail.com"
    port = 587
    s = smtplib.SMTP(host=host, port=port)
    s.starttls()
    s.login(email, password)
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = recipient
    msg['subject'] = subject
    msg.attach(MIMEText(body, "plain"))
    if path:
        for path in path:
            with open(path, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(path)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(path)
            msg.attach(part)

    s.send_message(msg)
    del msg
    s.quit()
