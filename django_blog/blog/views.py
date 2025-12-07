from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from .models import Post, UserProfile
from .forms import UserRegisterForm, UserUpdateForm

# Home view
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'blog/register.html', {'form': form})

# Custom Login View (optional - you can use Django's built-in view instead)
class CustomLoginView(LoginView):
    template_name = 'blog/login.html'
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)

# Profile View
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    # Get user's posts
    user_posts = Post.objects.filter(author=request.user)
    
    context = {
        'form': form,
        'user_posts': user_posts,
    }
    return render(request, 'blog/profile.html', context)

# User Profile Detail View (view other users' profiles)
def user_profile(request, username):
    try:
        user = UserProfile.objects.get(username=username)
        user_posts = Post.objects.filter(author=user)
        context = {
            'profile_user': user,
            'user_posts': user_posts,
        }
        return render(request, 'blog/user_profile.html', context)
    except UserProfile.DoesNotExist:
        messages.error(request, 'User does not exist.')
        return redirect('home')