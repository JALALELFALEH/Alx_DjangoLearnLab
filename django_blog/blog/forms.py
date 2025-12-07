from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from taggit.forms import TagWidget
from .models import Post, Comment

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
    password = None
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_id = self.instance.id
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            raise ValidationError("This email is already in use.")
        return email

class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas (e.g., django, python, web)'
        }),
        help_text='Separate tags with commas'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'is_published', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post content here...',
                'rows': 10
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            tags = self.instance.tags.names()
            self.initial['tags'] = ', '.join(tags)
    
    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        # Clean up tags: remove extra spaces, make lowercase
        tag_list = [tag.strip().lower() for tag in tags.split(',') if tag.strip()]
        return ', '.join(tag_list)
    
    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            # Clear existing tags and add new ones
            post.tags.clear()
            tags = self.cleaned_data.get('tags', '')
            if tags:
                tag_list = [tag.strip().lower() for tag in tags.split(',') if tag.strip()]
                post.tags.add(*tag_list)
            self.save_m2m()
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 4,
                'maxlength': 1000
            }),
        }
        labels = {
            'content': ''
        }

class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'maxlength': 1000
            }),
        }

class SearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control search-input',
            'placeholder': 'Search posts...',
            'aria-label': 'Search'
        }),
        label=''
    )
    
    search_in = forms.ChoiceField(
        required=False,
        choices=[
            ('all', 'All'),
            ('title', 'Title'),
            ('content', 'Content'),
            ('tags', 'Tags'),
            ('author', 'Author')
        ],
        widget=forms.RadioSelect(attrs={'class': 'search-options'}),
        initial='all',
        label='Search in:'
    )