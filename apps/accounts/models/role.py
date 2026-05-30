from django.db import models


class Role(models.Model):

    role_code = models.CharField(
        max_length=20,
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

    def __str__(self):
        return self.role_name