from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, LoginForm, CustomUserChangeForm, PostForm, CommentForm, SearchForm
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Follow, User
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model() 

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    comment_form = CommentForm()  # Initialize the comment form
    return render(request, 'post/home.html', {'posts': posts, 'comment_form': comment_form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # Important: request.FILES for images
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('home')  # Redirect to the home page (or wherever you want)
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')  # Redirect after successful login
            else:
                form.add_error(None, "Incorrect username or password")  # Add an error to the form
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')  # Redirect after logout

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect back to the profile page
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by('-created_at')

    # Check if the logged-in user follows the profile user
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, followed=user).exists()

    context = {
        'profile_user': user, # Use a different name to avoid confusion
        'posts': posts,
        'is_following': is_following,
    }


    return render(request, 'accounts/user_profile.html', context)

@login_required
def my_profile(request):
    return redirect('user_profile', username=request.user.username)

@login_required  # Only logged-in users can create posts
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Important: request.FILES for images
        if form.is_valid():
            post = form.save(commit=False)  # Don't save immediately
            post.user = request.user  # Set the user
            post.save()  # Now save
            return redirect('home')  # Redirect to home or wherever you want
    else:
        form = PostForm()
    return render(request, 'post/create_post.html', {'form': form})

@login_required
def add_comment(request, post_id,  parent_comment_id=None):
    post = get_object_or_404(Post, pk=post_id)  # Get the post or 404
    parent_comment = None
    if parent_comment_id:
        parent_comment = get_object_or_404(Comment, pk=parent_comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.parent_comment = parent_comment 
            comment.save()
            return redirect('post_detail', pk=post_id)  # Redirect to the post detail page
    else:
        form = CommentForm()
    return render(request, 'post/add_comment.html', {'form': form, 'post': post, 'parent_comment': parent_comment})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('created_at') # Get comments for the post
    comment_form = CommentForm() # Initialize comment form
    return render(request, 'post/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('home')

@login_required
def follow_user(request, user_id):
    followed_user = get_object_or_404(User, pk=user_id)
    if request.user != followed_user: # Prevent users from following themselves
        Follow.objects.get_or_create(follower=request.user, followed=followed_user)
    return redirect(request.META.get('HTTP_REFERER', 'home')) # Redirect back

@login_required
def unfollow_user(request, user_id):
    followed_user = get_object_or_404(User, pk=user_id)
    follow_relationship = Follow.objects.filter(follower=request.user, followed=followed_user).first()
    if follow_relationship:
        follow_relationship.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home')) # Redirect back

@login_required  # Only logged-in users can see their news feed
def news_feed(request):
    # Method 1 (More efficient for large numbers of followers):
    following_ids = request.user.following.values_list('followed_id', flat=True)  # Get IDs of followed users
    posts = Post.objects.filter(user__in=following_ids).order_by('-created_at')

    # Method 2 (Simpler, but potentially less efficient):
    # followed_users = request.user.following.all()  # Get the followed User objects
    # posts = Post.objects.filter(user__in=followed_users).order_by('-created_at')

    return render(request, 'posts/news_feed.html', {'posts': posts})

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by('-created_at')

    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, followed=user).exists()

    follower_count = Follow.objects.filter(followed=user).count() # Get follower count
    following_count = Follow.objects.filter(follower=user).count() # get following count

    context = {
        'profile_user': user,
        'posts': posts,
        'is_following': is_following,
        'follower_count': follower_count, # Add follower count to context
        'following_count': following_count, # Add following count to context
    }

    return render(request, 'accounts/user_profile.html', context)

# Optional: Add a view for the currently logged-in user's profile
@login_required
def my_profile(request):
    return redirect('user_profile', username=request.user.username)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.user == request.user:  # Check if the user owns the post
        post.delete()
    return redirect('home') 


def search(request):
    form = SearchForm(request.GET)
    users = []
    posts = []
    result_type = 'all' 

    if form.is_valid():
        query = form.cleaned_data['query']
        users = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ).distinct()
        posts = Post.objects.filter(Q(text__icontains=query)).distinct()

        if users and not posts:
            result_type = 'users'
        elif posts and not users:
            result_type = 'posts'

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'post/search_results.html', {'users': users, 'posts': posts, 'result_type': result_type})

    return render(request, 'post/search.html', {'form': form, 'users': users, 'posts': posts, 'result_type': result_type})