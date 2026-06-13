from django import forms
from .models import User, Role


class UserCreateForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())

    confirm_password = forms.CharField(widget=forms.PasswordInput())

    role = forms.ModelChoiceField(
        queryset=Role.objects.order_by('role_name'),
        empty_label='Select Role',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
    )

    class Meta:
        model = User

        fields = [
            'role',
            'designation',
            'employee_code',
            'full_name',
            'email',
            'username',
            'mobile_number',
            'department',
            'profile_image',
            'is_active',
        ]
        widgets = {
            'designation': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Designation',
                }
            ),
            'is_active': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:

            raise forms.ValidationError(
                'Passwords do not match.'
            )

        return cleaned_data
