from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    A form to handle the registration of the CustomUser model,
    using 'email' as the primary unique field.
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # The fields the user will fill out on registration
        fields = ('email', 'first_name', 'last_name', 'date_of_birth', 'profile_photo',)
        
    def save(self, commit=True):
        # We override save to ensure that the required 'username' field (by AbstractUser) 
        # is populated with the user's email before saving.
        user = super().save(commit=False)
        user.username = user.email 
        if commit:
            user.save()
        return user