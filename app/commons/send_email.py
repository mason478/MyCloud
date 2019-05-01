import smtplib
from email.mime.text import MIMEText


'''Send email'''


# class SendEmail:
#     def __init__(self):
#         self.mail_host = my_enums.MAIL_HOST
#         self.mail_user = my_enums.MAIL_USER_NAME
#         self.mail_pass = my_enums.MAIL_PASSWORD
#         self.mail_port = my_enums.MAIL_PORT
#         self.sender = my_enums.MAIL_EMAIL

    # @classmethod
    # def send(cls, msg, vendor='honda', receivers=[]):
    #     message = MIMEText(msg, 'html', 'utf-8')
    #     subject=Email_Subject_Map.get(vendor)
    #     if subject is None:
    #         subject='Unknown'
    #     message['Subject'] = subject
    #     message['From'] = cls().sender
    #     message['To'] = receivers[0]
    #     smtp = smtplib.SMTP()
    #     smtp.connect(host=cls().mail_host, port=cls().mail_port)
    #     smtp.login(user=cls().mail_user, password=cls().mail_pass)
    #     smtp.sendmail(from_addr=cls().sender, to_addrs=receivers, msg=message.as_string())

        # smtp.quit()
