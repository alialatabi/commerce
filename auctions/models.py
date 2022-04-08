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


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    start_price = models.FloatField(validators=[MinValueValidator(0.01)])
    image_url = models.CharField(null=True, max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    start_t = models.DateTimeField()
    end_t = models.DateTimeField()

    DURATIONS = (
        (2, "Two Days"),
        (5, "Five Days"),
        (10, "Ten Days"),
        (20, "Twenty Days")
    )

    duration = models.FloatField(default=2, choices=DURATIONS)

    class Meta:
        ordering = ('-end_t',)

    ended_manually = models.BooleanField(default=False)

    def __str__(self):
        return f"Auction #{self.id}: {self.title} ({self.user.username})"

    def save(self, *args, **kwargs):
        self.start_t = datetime.now()
        self.end_t = self.start_t + timedelta(days=self.duration)
        super().save(*args, **kwargs)

    def is_finished(self):
        if self.ended_manually or self.end_t < timezone.now():
            return True
        else:
            return False


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid = models.FloatField(default=0)
    date_and_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)


class Watch(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watch")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watch")
