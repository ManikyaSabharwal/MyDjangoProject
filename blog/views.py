from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm, CommentForm
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic import ListView
from django.core.paginator import Paginator


# Create your views here.

def post_list(request):
    all_posts = Post.objects.filter(published_date__lte = timezone.now()).order_by('published_date')
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=post)
        print(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user_comment = form.save(commit=False)
            user_comment.post_created_by = post.author
            user_comment.commented_by = request.user
            user_comment.comment = form.cleaned_data.get('comment')

            user_comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    args = { 'post': post, 'form': form}
    return render(request, 'blog/post_detail.html', args)

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        print(form, form.is_valid())
        if form.is_valid():
            post = form.save(commit=False)
            print(post, 1)
            post.author = request.user
            post.published_date = timezone.now()
            print(post, 2)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        print(request.POST)
        print(form.is_valid())
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


def post_upvote(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.upvotes_count += 1
    post.save()
    return redirect('post_list')
