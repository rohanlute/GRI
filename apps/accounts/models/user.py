from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    employee_code = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True
    )

    role = models.ForeignKey(
        'accounts.Role',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    mobile_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True
    )