from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib import admin

class User(AbstractUser):

    pass

class Auction_Listings(models.Model):
    username = models.CharField(max_length = 255)
    listing = models.CharField(max_length = 255)
    listing_price = models.DecimalField(max_digits=20, decimal_places=2)
    listing_description = models.CharField(max_length = 255)
    listing_url = models.CharField(max_length = 255)
    listing_category = models.CharField(max_length = 200)
    active = models.BooleanField(default = True)

    def __str__(self):
        return f'{self.username}, {self.listing}, {self.listing_price}, {self.listing_description}, {self.listing_url}, {self.listing_category}'
    pass

class Bids(models.Model):
    price = models.DecimalField(max_digits=16, decimal_places=2)
    listing = models.ForeignKey(Auction_Listings, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pass

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Auction_Listings, on_delete=models.CASCADE)
    comment = models.CharField(max_length = 255)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Auction_Listings, on_delete=models.CASCADE)

admin.site.register(Auction_Listings)
admin.site.register(Bids)
admin.site.register(Comments)