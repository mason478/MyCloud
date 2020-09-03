import smtplib
from email.mime.text import MIMEText

from app.commons.my_exception import SendEmailError
from app.commons.setting import MAIL_EMAIL, MAIL_HOST, MAIL_PASSWORD, MAIL_PORT,MAIL_USER_NAME
from app.commons.change_format import RET

'''Send email'''


class SendEmail:
    def __init__(self):
        self.mail_host = MAIL_HOST
        self.mail_user = MAIL_USER_NAME
        self.mail_pass = MAIL_PASSWORD
        self.mail_port = MAIL_PORT
        self.sender = MAIL_EMAIL

    @classmethod
    def send(cls, msg, subject=None, receivers=[]):
        message = MIMEText(msg, 'html', 'utf-8')
        if subject is None:
            subject = 'Unknown'
        message['Subject'] = subject
        message['From'] = cls().sender
        message['To'] = receivers[0]
        smtp = smtplib.SMTP()
        try:
            smtp.connect(host=cls().mail_host, port=cls().mail_port)
            smtp.login(user=cls().mail_user, password=cls().mail_pass)
            smtp.sendmail(from_addr=cls().sender, to_addrs=receivers, msg=message.as_string())
        except Exception as e:
            raise SendEmailError(error_code=RET.EMAIL_ERROR,error_msg=e)
        finally:
            smtp.quit()

if __name__=="__main__":
    try:
        SendEmail.send(msg='thi si a test',subject='Test',receivers=['13533801264@163.com'])
    except SendEmailError as e:
        print(e)
