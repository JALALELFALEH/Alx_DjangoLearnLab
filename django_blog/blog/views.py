from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.db.models import Q
from django.db import models
from taggit.models import Tag
from .models import Post, Comment, UserProfile
from .forms import UserRegisterForm, UserUpdateForm, PostForm, CommentForm, CommentUpdateForm, SearchForm
from django.contrib.auth.models import User

# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'blog/login.html'
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)

# Search View
def search_posts(request):
    form = SearchForm(request.GET or None)
    results = []
    query = ''
    search_in = 'all'
    
    if form.is_valid():
        query = form.cleaned_data.get('query', '').strip()
        search_in = form.cleaned_data.get('search_in', 'all')
        
        if query:
            # Start with all published posts
            posts = Post.objects.filter(is_published=True)
            
            # Build search queries based on search_in
            if search_in == 'all' or search_in == 'title':
                title_q = Q(title__icontains=query)
            else:
                title_q = Q()
            
            if search_in == 'all' or search_in == 'content':
                content_q = Q(content__icontains=query)
            else:
                content_q = Q()
            
            if search_in == 'all' or search_in == 'tags':
                tags_q = Q(tags__name__icontains=query)
            else:
                tags_q = Q()
            
            if search_in == 'all' or search_in == 'author':
                author_q = Q(author__username__icontains=query)
            else:
                author_q = Q()
            
            # Combine queries
            if search_in == 'all':
                q_object = title_q | content_q | tags_q | author_q
            elif search_in == 'title':
                q_object = title_q
            elif search_in == 'content':
                q_object = content_q
            elif search_in == 'tags':
                q_object = tags_q
            elif search_in == 'author':
                q_object = author_q
            else:
                q_object = Q()
            
            results = posts.filter(q_object).distinct().order_by('-published_date')
        else:
            results = Post.objects.filter(is_published=True).order_by('-published_date')[:10]
    
    context = {
        'form': form,
        'results': results,
        'query': query,
        'search_in': search_in,
        'result_count': len(results),
    }
    return render(request, 'blog/search_results.html', context)

# Tag View - Show posts by tag
class TagPostsListView(ListView):
    model = Post
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        tag = get_object_or_404(Tag, slug=tag_slug)
        
        if self.request.user.is_authenticated:
            return Post.objects.filter(
                Q(tags=tag) & 
                (Q(is_published=True) | Q(author=self.request.user))
            ).distinct().order_by('-published_date')
        
        return Post.objects.filter(tags=tag, is_published=True).order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug')
        context['tag'] = get_object_or_404(Tag, slug=tag_slug)
        return context

# Tag Cloud View
def tag_cloud(request):
    # Get all tags with count
    tags = Tag.objects.all()
    tag_data = []
    
    for tag in tags:
        count = Post.objects.filter(tags=tag, is_published=True).count()
        if count > 0:
            # Calculate font size based on count (logarithmic scale)
            min_size, max_size = 0.8, 2.0
            min_count = 1
            max_count = max(tags.annotate(post_count=models.Count('post')).values_list('post_count', flat=True))
            
            if max_count > min_count:
                scale = (max_size - min_size) / (max_count - min_count)
                size = min_size + (count - min_count) * scale
            else:
                size = (min_size + max_size) / 2
            
            tag_data.append({
                'tag': tag,
                'count': count,
                'size': f'{size:.1f}rem',
                'color': f'hsl({hash(tag.name) % 360}, 70%, 50%)'
            })
    
    # Sort by count (descending)
    tag_data.sort(key=lambda x: x['count'], reverse=True)
    
    context = {
        'tag_cloud': tag_data,
        'total_tags': len(tag_data),
    }
    return render(request, 'blog/tag_cloud.html', context)

# Post Views
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(
                models.Q(is_published=True) | 
                models.Q(author=self.request.user)
            ).order_by('-published_date')
        return Post.objects.filter(is_published=True).order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add popular tags to context
        popular_tags = Tag.objects.annotate(
            num_posts=models.Count('post')
        ).filter(num_posts__gt=0).order_by('-num_posts')[:10]
        context['popular_tags'] = popular_tags
        
        # Add search form to context
        context['search_form'] = SearchForm()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_active=True).order_by('-created_at')
        context['comment_form'] = CommentForm()
        context['comment_count'] = self.object.comment_count()
        context['related_posts'] = Post.objects.filter(
            author=self.object.author,
            is_published=True
        ).exclude(id=self.object.id)[:3]
        
        # Add search form to context
        context['search_form'] = SearchForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('home')
    context_object_name = 'post'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Your post has been deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Comment Views
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, 'Your comment has been added successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentUpdateForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Your comment has been updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.is_active = False  # Soft delete
        comment.save()
        messages.success(request, 'Your comment has been deleted successfully!')
        return redirect('post_detail', pk=comment.post.pk)
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})

# Quick add comment (for AJAX or inline form)
@login_required
def add_comment(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
        else:
            messages.error(request, 'Error adding comment. Please try again.')
    return redirect('post_detail', pk=pk)

# Authentication Views
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
    
    user_posts = Post.objects.filter(author=request.user)
    user_comments = Comment.objects.filter(author=request.user, is_active=True)
    
    context = {
        'form': form, 
        'user_posts': user_posts,
        'user_comments': user_comments,
        'search_form': SearchForm(),  # Add search form
    }
    return render(request, 'blog/profile.html', context)

def user_profile(request, username):
    try:
        user = User.objects.get(username=username)
        user_posts = Post.objects.filter(author=user, is_published=True)
        user_comments = Comment.objects.filter(author=user, is_active=True)
        context = {
            'profile_user': user, 
            'user_posts': user_posts,
            'user_comments': user_comments,
            'search_form': SearchForm(),  # Add search form
        }
        return render(request, 'blog/user_profile.html', context)
    except User.DoesNotExist:
        messages.error(request, 'User does not exist.')
        return redirect('home')