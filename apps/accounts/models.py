from django.db import models
from django.db.models import Q
from .models.user import User

# Create your models here.
class Department(models.Model):

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        app_label = 'accounts'

    def __str__(self):
        return f"{self.name} ({self.code})"

    def clean(self):
        if self.code:
            self.code = self.code.strip().upper()

    def save(self, *args, **kwargs):
        if self.code:
            self.code = self.code.strip().upper()
        super().save(*args, **kwargs)


    @property
    def employee_count(self):
        return self.users.count()

    @property
    def active_employee_count(self):
        return self.users.filter(is_active=True).count()
