from os import name
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
    current_user = request.user
    profile = Profile.objects.filter(
        user_id=current_user.id).first()  # get profile
    posts = Post.objects.filter(user_id=current_user.id)
    # get all locations
    locations = Location.objects.all()
    neighbourhood = NeighbourHood.objects.all()
    category = Category.objects.all()
    return render(request, 'profile.html', {'profile': profile, 'posts': posts, 'locations': locations, 'neighbourhood': neighbourhood, 'categories': category})


# update profile
@login_required(login_url="/accounts/login/")
def update_profile(request):
    if request.method == "POST":

        current_user = request.user

        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]

        name = request.POST["first_name"] + " " + request.POST["last_name"]

        neighbourhood = request.POST["neighbourhood"]
        location = request.POST["location"]

        # check if its an instance of location
        if location == "":
            location = None
        else:
            location = Location.objects.get(name=location)

        # check if its an instance of neighbourhood
        if neighbourhood == "":
            neighbourhood = None
        else:
            neighbourhood = NeighbourHood.objects.get(name=neighbourhood)

        profile_image = request.FILES["profile_pic"]
        profile_image = cloudinary.uploader.upload(profile_image)
        profile_url = profile_image["url"]

        user = User.objects.get(id=current_user.id)

        # check if user exists in profile table and if not create a new profile
        if Profile.objects.filter(user_id=current_user.id).exists():

            profile = Profile.objects.get(user_id=current_user.id)
            profile.profile_pic = profile_url
            profile.neighbourhood = neighbourhood
            profile.location = location
            profile.save()
        else:
            profile = Profile(
                user_id=current_user.id,
                name=name,
                profile_pic=profile_url,
                neighbourhood=neighbourhood,
                location=location,
            )

            profile.save_profile()

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        user.save()

        return redirect("/profile", {"success": "Profile Updated Successfully"})

        # return render(request, 'profile.html', {'success': 'Profile Updated Successfully'})
    else:
        return render(request, "profile.html", {"danger": "Profile Update Failed"})


# create post
@login_required(login_url="/accounts/login/")
def create_post(request):
    if request.method == "POST":
        current_user = request.user
        title = request.POST["title"]
        content = request.POST["content"]
        category = request.POST["category"]
        location = request.POST["location"]
        # neighbourhood = request.POST["neighbourhood"]

         # check if its an instance of category
        if category == "":
            category = None
        else:
            category = Category.objects.get(name=category)

         # check if its an instance of location
        if location == "":
            location = None
        else:
            location = Location.objects.get(name=location)

        # check if there is a post with image 
        if request.FILES:
            image = request.FILES["image"]
            image = cloudinary.uploader.upload(image)
            image_url = image["url"]

            post = Post(
                user_id=current_user.id,
                title=title,
                content=content,
                image=image_url,
                category=category,
                location=location,
            )
            post.create_post()

            return redirect("/profile", {"success": "Post Created Successfully"})
        else:
            post = Post(
                user_id=current_user.id,
                title=title,
                content=content,
                category=category,
                location=location,
            )
            post.save_post()

            return redirect("/profile", {"success": "Post Created Successfully"})

    #     image = request.FILES["image"]


    #     # check if its an instance of location
    #     if location == "":
    #         location = None
    #     else:
    #         location = Location.objects.get(name=location)

    #     # check if its an instance of neighbourhood
    #     # if neighbourhood == "":
    #     #     neighbourhood = None
    #     # else:
    #     #     neighbourhood = NeighbourHood.objects.get(name=neighbourhood)

       

    #     # check if user has a profile
    #     if Profile.objects.filter(user_id=current_user.id).exists():
    #         profile = Profile.objects.get(user_id=current_user.id)
    #         post = Post(
    #             user_id=current_user.id,
    #             profile_id=profile.id,
    #             title=title,
    #             post=post,
    #             category=category,
    #             location=location,
    #             neighbourhood=neighbourhood,
    #         )
    #         post.save_post()
    #         return redirect("/profile", {"success": "Post Created Successfully"})
    #     else:
    #         return redirect("/profile", {"danger": "Please Update Your Profile"})
    # else:
    #     return render(request, "profile.html", {"danger": "Post Creation Failed"})