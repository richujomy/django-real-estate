

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(
        max_length=10,
        choices=[('user', 'User'), ('admin', 'Admin')],
        default='user'
    )
    # Avoid conflicts with Django's default auth system
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",  # Change related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions_set",  # Change related_name
        blank=True
    )

    def str(self):
        return self.username  # Change from self.email to self.username if email is not a unique identifier

    
    