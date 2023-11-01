from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, Page
from .models import *


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
@login_required
def addpost(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    posttext = data.get("posttext")
    print(posttext)
    post = NetPost(text=posttext, user=request.user)
    post.save()
    return JsonResponse({"message": "Post sent successfully."}, status=201)


def getposts(request):
    ''' url = request.build_absolute_uri()
    print(f'URL: {url}')
    print(request.GET)'''
    page_number = int(request.GET.get('page', 1))
    print(f'pagenumber is {page_number}')

    items_per_page = 10
    paginator = Paginator(NetPost.objects.order_by(
        '-timestamp'), items_per_page)
    page = paginator.get_page(page_number)

    data = {
        # Serialize your items to JSON
        'posts': [item.serialize() for item in page],
        'current_page': page.number,
        'total_pages': paginator.num_pages,
    }
    return JsonResponse(data)


@csrf_exempt
@login_required
def display_posts(request):
    ''' url = request.build_absolute_uri()
    print(f'URL: {url}')
    print(request.GET)'''
    page_number = int(request.GET.get('page', 1))
    print(f'pagenumber is {page_number}')

    items_per_page = 10
    paginator = Paginator(NetPost.objects.order_by(
        '-timestamp'), items_per_page)
    page = paginator.get_page(page_number)
    print(f'Page object: {page}')
    for post in page:
        print(post)
    return render(request, 'network/index1.html', {'posts': page})
