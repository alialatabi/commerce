from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "comments": Comment.objects.all()
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def category(request):
    return render(request, "auctions/category.html", {
        'categories': Category.objects.all()
    })


@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watches": Watch.objects.all()
    })


@login_required
def create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        cat = request.POST.get('category')
        cat = Category.objects.get(category=cat)
        image = request.POST.get('img_url')
        user = request.user
        Listing.objects.create(title=title, description=description,
                               start_price=price, category=cat,
                               image_url=image, user=user)
    return render(request, "auctions/create.html", {
        "listings": Listing.objects.all(),
        'categories': Category.objects.all()
    })


def show(request, l_id):
    listing = Listing.objects.get(id=l_id)
    bids = Bid.objects.filter(listing=listing)
    user = request.user
    current_bid = 0
    err = ''
    my_listing = False
    if bids:
        for bid in bids:
            if bid.bid > current_bid:
                current_bid = bid.bid
    else:
        current_bid = 'No Bids Yet'
    if user:
        if listing.user == user:
            my_listing = True

    if request.POST:
        if user != listing.user:
            bid_price = request.POST.get('bid_price')
            if bids:
                if float(bid_price) > current_bid:
                    Bid.objects.create(listing=listing,
                                       user=user,
                                       bid=bid_price)
                    current_bid = bid_price
                else:
                    err = "The current largest bid is bigger than your bid!!!"
            else:
                if float(bid_price) > listing.start_price:
                    Bid.objects.create(listing=listing,
                                       user=user,
                                       bid=bid_price)
                else:
                    err = "Your bid is smaller than the starting price"
        else:
            err = "You Can't bid on your own Listing"

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": bids,
        "current_bid": current_bid,
        "err": err,
        "my_listing": my_listing,
        "current_user": user
    })


def close(request, l_id):
    if request.POST:
        listing = Listing.objects.get(id=l_id)
        listing.is_closed = True
        listing.save()

    return HttpResponseRedirect(reverse('show', args=(l_id,)))


def cat_listings(request, cat_id):
    listings = Listing.objects.filter(category=cat_id)
    return render(request, "auctions/index.html", {
        "listings": listings,
    })