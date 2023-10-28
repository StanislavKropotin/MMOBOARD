from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Article, UserResponse


@receiver(post_save, sender=Article)
def product_created(instance, created, **kwargs):
    if not created:
        return
    emails = User.objects.filter(
    ).values_list('email', flat=True)
    subject = f'Новое объявление в категории {instance.category}'

    text_content = (
        f'Объявление: {instance.text}\n'
        f'Ссылка на объявление: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Объявление: {instance.text}<br>'
        
        f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
        f'Ссылка на объявление</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@receiver(post_save, sender=UserResponse)
def response_created(instance, created, **kwargs):
    if not created:
        return

    send_mail(
        subject='Реакция на Ваше объявление!',
        message=f'Реакция:{instance.text}, Вам отклик от {instance.author}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[instance.article.author.email],
    )

