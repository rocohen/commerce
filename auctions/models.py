from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    categoryImage = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=280)
    imageURL = models.URLField(blank=True, default="https://www.flaticon.com/svg/static/icons/svg/2598/2598023.svg")
    startingBid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="listings_category")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    creationDate = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f" {self.title}, created by {self.author}. Bid price: {self.startingBid}"

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenters")
    content = models.TextField(max_length=500)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="items_commented")
    commentDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commenter} has commented on {self.listing}"

class Bid(models.Model):
    amountBid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    bidder = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="user_bid")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    
    def __str__(self):
        return f"{self.bidder}: has bid {self.amountBid} on {self.listing}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchers") 
    listings = models.ManyToManyField(Listing, blank=True, related_name="watchlistItems" )


    def __str__(self):
        return f"{self.user} is currently watching {self.listings.count()} listing(s)"