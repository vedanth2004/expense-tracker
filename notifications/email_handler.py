import smtplib
from email.mime.text import MIMEText

class EmailHandler:
    def __init__(self, settings):
        self.host = settings.smtp_host
        self.port = settings.smtp_port
        self.user = settings.smtp_user
        self.password = settings.smtp_pass

    def send_test(self, to_email: str, subject: str, body: str) -> bool:
        if not self.user or not self.password or not self.host:
            return False
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.user
        msg["To"] = to_email
        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.sendmail(self.user, [to_email], msg.as_string())
            return True
        except Exception:
            return False
