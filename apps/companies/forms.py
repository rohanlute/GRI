from django import forms
from .models import Company


class CompanyForm(forms.ModelForm):
    company_logo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'file-upload',
                'accept': 'image/*',
                'style': 'position:absolute; inset:0; width:100%; height:100%; opacity:0; cursor:pointer; z-index:2;',
            }
        ),
    )

    class Meta:
        model = Company
        fields = [
            'company_logo',
            'company_name',
            'email',
            'mobile_number',
            'website',
            'gst_number',
            'about_company',
            'is_active',
        ]
        widgets = {
            'company_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Company',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Email',
                }
            ),
            'mobile_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Phone',
                }
            ),
            'website': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Website',
                }
            ),
            'gst_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'GST',
                }
            ),
            'about_company': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'About',
                    'rows': 5,
                }
            ),
            'is_active': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
        }
