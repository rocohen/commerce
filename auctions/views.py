from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import * 

from .models import User, Category, Listing, Comment, Bid, Watchlist

def index(request):
    listings = Listing.objects.exclude(active=False).all().order_by('-id')
    context = {'listings': listings}
    return render(request, "auctions/index.html", context)


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

# Create a new listing
@login_required(login_url='login')
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.author = request.user
            new_listing.save()
            return HttpResponseRedirect(reverse("index"))   
        else:
            return render(request, "auctions/create_listing.html", {
                "form": form
            })
    
    return render(request, "auctions/create_listing.html", {
            "form": ListingForm()
        })


@login_required(login_url='login')
def display_watchlist(request):
    if request.POST.get('unwatch_item'):
            listing = request.POST.get('unwatch_item')
            watchlist = Watchlist.objects.get(user=request.user)
            watchlist.listings.remove(listing)
            return HttpResponseRedirect(reverse("watchlist"))
    return render(request, "auctions/watchlist.html")

@login_required(login_url='login')
def get_categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", { "categories": categories })

@login_required(login_url='login')
def display_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    category_listings = Listing.objects.filter(category=category, active=True).all().order_by('-id')
    print(category_listings)
    return render(request, "auctions/category.html", { "category_listings": category_listings, "category": category })


def get_listing(request, listing_id):   
    comments = Comment.objects.filter(listing=listing_id).all()
    listing = Listing.objects.get(pk=listing_id)
    current_bid = listing.startingBid
    bids = listing.bids.all() 
    last_bid = listing.bids.last()
    auction_winner = None
    watchlist_item = None
    creator = False

    # Forms
    commentForm = CommentForm(initial={'content': 'Your comment...'})
    bidForm = BidForm()

    # Check if user is watching a listing
    if request.user.is_authenticated:
        watchlist_item = Watchlist.objects.filter(user=request.user, listings=listing)
    
    
    # Check if current user has created the auction
    if listing.author == request.user:
       creator = True
        
    
    # Check if current user is trying to comment, place a bid or close an auction
    if request.POST:
        if request.POST.get('form') == 'comment_form':
            if not request.user.is_authenticated:
                messages.error(request, 'You should sign in to post a comment!')
            else:
                form = CommentForm(request.POST)
                if form.is_valid():
                    new_comment = form.save(commit=False)
                    new_comment.commenter = request.user
                    new_comment.listing = listing
                    new_comment.save()

                    messages.success(request, 'Your comment has been added!')
                    return HttpResponseRedirect(reverse("listing", args=(listing.id, )))
           
        elif request.POST.get('form') == 'bid_form': 
            if not request.user.is_authenticated:
                messages.error(request, 'You should sign in to place a bid!')      
            else:
                form = BidForm(request.POST)
                if form.is_valid() and float(request.POST['amountBid']) > float(current_bid):
                    current_bid = form.save(commit=False)
                    current_bid.bidder = request.user
                    current_bid.listing = listing
                    current_bid.save()
                    current_bid = Listing.objects.filter(pk=listing_id).update(startingBid=float(request.POST['amountBid']))
                    
                    messages.success(request, 'Your bid has been successfully placed! Your bid is the current bid.')
                    return HttpResponseRedirect(reverse("listing", args=(listing.id, )))

                else:
                    messages.error(request, 'Your bid should be greater than the current bid price. Please try again!')

        # Close auction
        elif request.POST.get('closeAuction') and creator:
            Listing.objects.filter(pk=listing_id).update(active=False)
            return HttpResponseRedirect(reverse("listing", args=(listing.id, )))
        
        # Watching and unwatching a listing
        elif request.POST.get('watch_item'):
            if not request.user.is_authenticated:
                messages.error(request, 'You should sign in to add an item to a watchlist!')
            else:
                watchlist, created = Watchlist.objects.get_or_create(user=request.user)
                watchlist.listings.add(listing)
                return HttpResponseRedirect(reverse("listing", args=(listing.id, )))

        elif request.POST.get('unwatch_item'):
            watchlist = Watchlist.objects.get(user=request.user)
            watchlist.listings.remove(listing)
            return HttpResponseRedirect(reverse("listing", args=(listing.id, )))

    # Check auction winner
    if request.user.is_authenticated and last_bid != None:
        closed_auction = Listing.objects.filter(pk=listing_id , active=False)
        if request.user == last_bid.bidder and closed_auction:
            auction_winner = last_bid.bidder
            
            

    context = { 
        "listing": listing,
        "creator": creator,
        "comments": comments,
        "commentForm": commentForm,
        "bidForm": bidForm,
        "bids": bids,
        "last_bid": last_bid,
        "watchlist_item": watchlist_item,
        "auction_winner": auction_winner
    }
    return render(request, "auctions/listing.html", context)

@login_required(login_url='login')
def closed_auctions(request):
    closed_auctions = Listing.objects.filter(active=False).all()
    return render(request, "auctions/closed_auctions.html", { "closed_auctions": closed_auctions })