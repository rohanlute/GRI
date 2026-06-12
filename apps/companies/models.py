from django.db import models


class Company(models.Model):
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    company_code = models.CharField(max_length=20, unique=True)
    company_name = models.CharField(max_length=255)
    gst_number = models.CharField(max_length=50, blank=True, null=True)
    about_company = models.TextField(blank=True, null=True)
    company_password_hash = models.CharField(max_length=128, blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    billing_zip_code = models.CharField(max_length=20, blank=True, null=True)
    billing_country = models.CharField(max_length=100, blank=True, null=True)
    billing_state = models.CharField(max_length=100, blank=True, null=True)
    billing_city = models.CharField(max_length=100, blank=True, null=True)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    industry_type = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    module_access_brsr = models.BooleanField(default=False)
    module_access_gri = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_code} - {self.company_name}"