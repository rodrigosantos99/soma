from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from django.dispatch import receiver
import os

from .utils import (
    generate_student_credentials,
    generate_lecturer_credentials,
    send_new_account_email,
)


def post_save_account_receiver(instance=None, created=False, *args, **kwargs):
    """
    Send email notification to new students or lecturers
    """
    if created:
        if instance.is_student:
            username, password = generate_student_credentials()
            instance.username = username
            instance.set_password(password)
            instance.save()
            send_new_account_email(instance, password)

        if instance.is_lecturer:
            username, password = generate_lecturer_credentials()
            instance.username = username
            instance.set_password(password)
            instance.save()
            send_new_account_email(instance, password)


@receiver(post_migrate)
def create_admin_user(sender, **kwargs):
    """
    Automatically creates a superuser after initial migration
    if it doesn't exist, using environment variables.
    """
    User = get_user_model()
    username = os.environ.get("ADMIN_USERNAME", "admin")
    email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
    password = os.environ.get("ADMIN_PASSWORD", "senha123")

    if not User.objects.filter(username=username).exists():
        print(f"⚙️  Creating superuser '{username}'...")
        User.objects.create_superuser(username, email, password)
