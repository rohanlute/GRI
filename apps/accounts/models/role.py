from django.db import models
from apps.accounts.models.permission import Permissions


class Role(models.Model):

    role_code = models.CharField(
        max_length=30,
        unique=True
    )

    role_name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    permissions = models.ManyToManyField(
        Permissions,
        related_name='roles',
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.role_name