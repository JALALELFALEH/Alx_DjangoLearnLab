from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserUpdateForm(UserChangeForm):
    password = None  # Remove password field from the form
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_id = self.instance.id
        
        # Check if email is already taken by another user
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            raise ValidationError("This email is already in use.")
        return email