from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
import random


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    code = random.randint(1000, 9999)
    reset_password_token.key = str(code)
    reset_password_token.save()

    send_mail(
        "Сброс пароля",
        f"Ваш код для сброса пароля: {code}",
        "noreply@example.com",
        [reset_password_token.user.email],
        fail_silently=False,
    )


