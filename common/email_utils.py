from django.core.mail import send_mail

from vmc_backend import settings


def send_email(to, subject, message):
    if settings.DEBUG:
        print("发送邮件,to={},subject={},message={}".format(to, subject, message))
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to],
    )
