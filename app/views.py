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
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})


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
    businesses = Business.objects.filter(user_id=current_user.id)
    contacts = Contact.objects.filter(user_id=current_user.id)
    return render(request, 'profile.html', {'profile': profile, 'posts': posts, 'locations': locations, 'neighbourhood': neighbourhood, 'categories': category, 'businesses': businesses, 'contacts': contacts})


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
            # upload image to cloudinary and crop it to square
            image = cloudinary.uploader.upload(
                image, crop="limit", width=800, height=600)
            # image = cloudinary.uploader.upload(image)
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
            post.create_post()

            return redirect("/profile", {"success": "Post Created Successfully"})


# create business
@login_required(login_url="/accounts/login/")
def create_business(request):
    if request.method == "POST":
        current_user = request.user
        name = request.POST["name"]
        email = request.POST["email"]
        # phone = request.POST["phone"]
        # address = request.POST["address"]
        # location = request.POST["location"]
        neighbourhood = request.POST["neighbourhood"]

        # check if its an instance of location
        # if location == "":
        #     location = None
        # else:
        #     location = Location.objects.get(name=location)

        # check if its an instance of neighbourhood
        if neighbourhood == "":
            neighbourhood = None
        else:
            neighbourhood = NeighbourHood.objects.get(name=neighbourhood)

        business = Business(
            user_id=current_user.id,
            name=name,
            email=email,
            # phone=phone,
            # address=address,
            # location=location,
            neighbourhood=neighbourhood,
        )
        business.create_business()

        return redirect("/profile", {"success": "Business Created Successfully"})
    else:
        return render(request, "profile.html", {"danger": "Business Creation Failed"})


# create contact
@login_required(login_url="/accounts/login/")
def create_contact(request):
    if request.method == "POST":
        current_user = request.user
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        neighbourhood = request.POST["neighbourhood"]

        # # check if its an instance of location
        # if location == "":
        #     location = None
        # else:
        #     location = Location.objects.get(name=location)

        # check if its an instance of neighbourhood
        if neighbourhood == "":
            neighbourhood = None
        else:
            neighbourhood = NeighbourHood.objects.get(name=neighbourhood)

        contact = Contact(
            user_id=current_user.id,
            name=name,
            email=email,
            phone=phone,
            neighbourhood=neighbourhood,
        )
        contact.create_contact()

        return redirect("/profile", {"success": "Contact Created Successfully"})
    else:
        return render(request, "profile.html", {"danger": "Contact Creation Failed"})


@login_required(login_url="/accounts/login/")
# posts page
def posts(request):
    # get all posts and order by date
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "posts.html", {"posts": posts})


@login_required(login_url="/accounts/login/")
# alerts page
def alerts(request):
    # get the category that contains name "alerts"
    category = Category.objects.get(name="alerts")
    # get all posts that contains the word "alert" and order by date
    posts = Post.objects.filter(category=category).order_by("-created_at")
    return render(request, "alerts.html", {"posts": posts})


# business page
@login_required(login_url="/accounts/login/")
def business(request):
    # get current user
    current_user = request.user
    # get user neighbourhood
    profile = Profile.objects.filter(user_id=current_user.id).first()
    # check if user has profile
    if profile:
        # get all businesses in the user neighbourhood
        businesses = Business.objects.filter(
            neighbourhood=profile.neighbourhood)
        return render(request, "business.html", {"businesses": businesses})
    else:
        return render(request, "business.html", {"businesses": None})


# contact page
@login_required(login_url="/accounts/login/")
def contacts(request):
    # get current user
    current_user = request.user
    # get user neighbourhood
    profile = Profile.objects.filter(user_id=current_user.id).first()
    # check if user has profile
    if profile:
        # get all contacts where the neighbourhood is the same as the user neighbourhood
        contacts = Contact.objects.filter(
            neighbourhood=profile.neighbourhood).order_by("-created_at")
        return render(request, "contacts.html", {"contacts": contacts, "neighbourhood": profile.neighbourhood})
    else:
        contacts = Contact.objects.all().order_by("-created_at")
        return render(request, "contacts.html", {"contacts": contacts, "neighbourhood": None})


# search 
@login_required(login_url="/accounts/login/")
def search(request):
    if 'search_term' in request.GET and request.GET["search_term"]:
        search_term = request.GET.get("search_term")
        searched_posts = Post.objects.filter(title__icontains=search_term)
        message = f"Search For: {search_term}"

        return render(request, "search.html", {"message": message, "posts": searched_posts})
    else:
        message = "You haven't searched for any term"
        return render(request, "search.html", {"message": message})
