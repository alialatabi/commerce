from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Category(models.Model):
    category = models.CharField(null=True, max_length=64)

    def __str__(self):
        return f"{self.category}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    start_price = models.FloatField(validators=[MinValueValidator(0.01)])
    image_url = models.URLField(max_length=200, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid = models.FloatField(default=0)
    date_and_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.listing.title} || {self.bid}"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.listing.title} || {self.comment}"


class Watch(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watch")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watch")
