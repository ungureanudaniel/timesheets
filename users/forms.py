from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth import get_user_model # why this here?
from django.utils.translation import gettext_lazy as _

User = get_user_model() # why this?

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            # Apply Bootstrap classes and custom styles to form fields
            self.fields['username'].widget.attrs.update({
                'class': 'form-control w-100',
                'placeholder': _('Enter username'),
            })
            self.fields['email'].widget.attrs.update({
                'class': 'form-control d-flex p-2 bd-highlight',
                'placeholder': _('Enter email'),
            })
            self.fields['password1'].widget.attrs.update({
                'class': 'form-control d-flex p-2 bd-highlight',
                'placeholder': _('Enter password'),
            })
            self.fields['password2'].widget.attrs.update({
                'class': 'form-control d-flex p-2 bd-highlight',
                'placeholder': _('Confirm password'),
            })

        def save(self, commit=True):
            user = super().save(commit=False)
            user.is_approved = False  # Set new user as unapproved by default
            if commit:
                user.save()
                user.assign_initial_group()
            return user

        