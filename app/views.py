from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
import cloudinary
import cloudinary.uploader
import cloudinary.api


# index view
@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, 'index.html')


# profile view
@login_required(login_url='/accounts/login/')
def profile(request):
    user = request.user
    profile = User.objects.get(user=user)
    posts = Post.objects.filter(user=user)
    return render(request, 'profile.html', {'profile': profile, 'posts': posts})
