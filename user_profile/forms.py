from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class UserProfileForm(forms.ModelForm):
    current_password = forms.CharField(widget=forms.PasswordInput(), required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'current_password', 'new_password', 'confirm_password']
        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'current_password': 'Current password',
            'new_password': 'New password',
            'confirm_password': 'Confirm password',
        } 

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        # Check if the current password is correct
        if current_password and not authenticate(username=self.instance.username, password=current_password):
            self.add_error('current_password', 'Current password is incorrect.')

        # Check if new password and confirm password match
        if new_password and new_password != confirm_password:
            self.add_error('confirm_password', "New password and Confirm password do not match.")
        
        # Validate the new password
        if new_password:
            try:
                validate_password(new_password, self.instance)
            except ValidationError as error:
                self.add_error('new_password', error)

        return cleaned_data
