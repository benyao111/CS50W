from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from django.contrib.auth.decorators import login_required

def index(request):
    if request.method == "POST":
        form = request.POST
        Auction_Listings.objects.create(username = request.user.username, listing = form['title'],
                                        listing_description = form['description'], listing_price = form['starting_bid'],
                                        listing_url = form['image_url'], listing_category = form['category'])
        #print(Auction_Listings.objects.all())
        return render(request, "auctions/index.html", {
            "Auction_Listings": Auction_Listings.objects.filter(active = True)
        })

    return render(request, "auctions/index.html", {
        "Auction_Listings": Auction_Listings.objects.filter(active = True)
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
def createlisting(request):
    if request.method == "POST":

        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/createlisting.html")

#@login_required, dont need this otherwise you cant see the listings if not logged in and we need the page to still render even if not logged in
def listing(request, i):
    #specific info being passed by the i after %url 'listing' i.id% in index.html. Cant pass whole object into i. Django has their own autoincrement called .id
    auction_listing = Auction_Listings.objects.get(id=i)
    bids = Bids.objects.filter(listing = auction_listing)
    user = request.user
    listofids = []
    message = ""
    commentlist = Comments.objects.filter(listing=auction_listing)
    winner = bids.order_by('-price').first()
    try:
        for i in Watchlist.objects.filter(user=request.user):
            listofids.append(i.listing.id)
    except:
        pass
    if request.method == "POST":
        '''Place Bid.If the user is signed in, the user should be able to bid on the item.
        The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any).
        If the bid doesn’t meet those criteria, the user should be presented with an error.'''
        try:
            if float(request.POST['bid']) > float(auction_listing.listing_price):
                auction_listing.listing_price = request.POST['bid']
                auction_listing.save()
                Bids.objects.create(user=request.user, listing=auction_listing, price=request.POST['bid'])
                message = "Bid placed"
            else:
                message = 'Please enter a bid greater than the current one.'

        except:
            Comments.objects.create(user=request.user, listing=auction_listing, comment=request.POST['comment'])
            commentlist = Comments.objects.filter(listing=auction_listing)



        return render(request, "auctions/listing.html", {
            "Auction_Listing": auction_listing,
            "user": user,
            "watchlist": listofids,
            "message": message,
            "commentlist": commentlist,
            'winner': winner
        })

    return render(request, "auctions/listing.html",{
        "Auction_Listing": auction_listing,
        "user": user,
        "watchlist": listofids,
        'message': message,
        "commentlist": commentlist,
        'winner': winner
    })


def watchlist(request):
    if request.method == "POST":
        # could do a try/except thing to check for request.POST['listing_id_remove']
        #instance = SomeModel.objects.get(id=id), then instance.delete() to delete that entry in watchlist model.
        try:
            i = request.POST['listing_id']
            Watchlist.objects.create(user=request.user, listing=Auction_Listings.objects.get(id=i)) #add the listing_id and pair it with the user who wants to add it to his/her watchlist.
            return render(request, "auctions/watchlist.html",
                       {'watchlist': Watchlist.objects.filter(user=request.user)
            })
        except:
            i = request.POST['listing_id_remove']
            instance = Watchlist.objects.get(user=request.user, listing=Auction_Listings.objects.get(id=i))
            instance.delete()
            return render(request, "auctions/watchlist.html",
                       {'watchlist': Watchlist.objects.filter(user=request.user)
            })

    return render(request, "auctions/watchlist.html",{
        'watchlist': Watchlist.objects.filter(user=request.user)
    })

def categories(request):

    #users should be able to visit a page that displays a list of all listing categories.
    #Clicking on the name of any category should take the user to a page that displays all of the active listings in that category.
    if request.method == "POST":
        response = request.POST['category']
        return render(request, "auctions/categories.html", {
            "Auction_Listings": Auction_Listings.objects.filter(listing_category=response)
        })

    return render(request, "auctions/categories.html", {
    })


#If the user is signed in and is the one who created the listing, the user should have the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
#If a user is signed in on a closed listing page, and the user has won that auction, the page should say so.

def closeauctionlisting(request, i):
    auction_listing = Auction_Listings.objects.get(id=i)
    if request.method == "POST" and auction_listing.active == True:
        auction_listing.active = False
        auction_listing.save()
    elif request.method == "POST" and auction_listing.active == False:
        auction_listing.active = True
        auction_listing.save()
    
    return HttpResponseRedirect(reverse('listing', args =(i)))



