from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms    

from .models import User,Categories,Listings,Comments,Bids,WatchList

from datetime import datetime


def index(request):
    listings = Listings.objects.all()
    return render(request, "auctions/index.html",{
        "listings" : listings
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

class BidForm(forms.Form):
    bid = forms.IntegerField(label = "Bid Amount")

class CommentForm(forms.Form):
    comment = forms.CharField(widget = forms.Textarea(attrs={"rows":5, "cols":122}), label = "")

def create_item(request):
    categories = Categories.objects.all()
    return render(request,"auctions/create.html", {
        "categories" : categories
    })

def submit(request):
    if request.method == "POST":
        it_name = request.POST.get('it_name')
        it_desc = request.POST.get('it_desc')
        it_seller = request.user.username
        starting_bid = request.POST.get('starting_bid')
        current_bid = str(int(starting_bid) - 1)
        category = request.POST.get('category')
        
        if request.POST.get('img_url'):
            img_url = request.POST.get('img_url')
        else: img_url = "NULL"

        newEntry = Listings(
            it_name = it_name, 
            it_desc = it_desc, 
            it_seller = it_seller, 
            starting_bid = starting_bid,
            current_bid = current_bid,
            category = category,
            img_url = img_url
        )
        
        newEntry.save()

    return HttpResponseRedirect(reverse("index"))

def view_listing(request, id):
    listing = Listings.objects.get(id = id)
    try:
        if WatchList.objects.get(watcher = request.user.username, list_id = id):
            watching = True
    except:
        watching = False

    try:
        comments = Comments.objects.filter(list_id = id)
    except:
        comments = None

    return render(request,"auctions/listinginfo.html",{
        "listing" : listing,
        "watchinguser" : request.user.username,
        "watching" : watching,
        "comments" : comments,
        "form" : BidForm(),
        "form2" : CommentForm(),
        "alert" : False
    })

def add_watchlist(request,id):
    if request.user.username:
        newItm = WatchList(watcher = request.user.username, list_id = id)
        newItm.save()
    return redirect('listing', id = id)

def rem_watchlist(request,id):
    if request.user.username:
        try:
            delItm = WatchList.objects.get(watcher=request.user.username, list_id = id)
            delItm.delete()
        except:
            pass

    return redirect('listing', id = id)

def view_watchlist(request):
    listings = Listings.objects.all()

    itmList = WatchList.objects.filter(watcher = request.user.username)

    return render(request,"auctions/ViewWatchlist.html",{
        "Listings" : listings,
        "WatchList" : itmList
    })

def make_bid(request,id):
    listing = Listings.objects.get(id = id)

    curr_bid = listing.current_bid

    if request.method == "POST":
        bid = int(request.POST.get('bid'))
        if(bid > curr_bid):
            listing.current_bid = bid
            listing.bid_winner = request.user.username
            listing.save()

            try:
                wlistObj = WatchList.objects.get(watcher = request.user.username, list_id = id)
            except:
                newItm = WatchList(watcher = request.user.username, list_id = id)
                newItm.save()

            newBid = Bids(bid = bid, list_id = id, user = request.user.username)
            newBid.save()   
            return redirect('listing', id = id)
        else:
            listing = Listings.objects.get(id = id)

            try:
                if WatchList.objects.get(watcher = request.user.username, list_id = id):
                    watching = True
            except:
                watching = False

            return render(request,"auctions/listinginfo.html",{
                "listing" : listing,
                "watching" : watching,
                "form" : BidForm(),
                "form2" : CommentForm(),
                "alert" : True
            })

def close_bid(request,id):
    listing = Listings.objects.get(id = id)
    listing.active = False
    listing.save()

    return redirect('listing', id = id)

def categories(request):
    catList = Listings.objects.values('category').distinct()

    return render(request, "auctions/categories.html",{
        "categories" : catList
    })

def catview(request,catname):
    listings = Listings.objects.filter(category = catname)
    title = catname

    return render(request,"auctions/index.html",{
        "listings" : listings,
        "title" : title 
    })

def make_comment(request,id):
    comment = request.POST.get('comment')
    time = datetime.now().strftime("%m / %d / %Y %I: %M %p")
    if request.method == "POST":
        newcomment = Comments(comment = comment, list_id = id, user = request.user.username, posting_time = time)
        newcomment.save()
        return redirect('listing',id = id)

