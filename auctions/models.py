from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    it_name = models.CharField(max_length = 64)
    it_desc = models.CharField(max_length = 100)
    it_seller = models.CharField(max_length = 64)
    bid_winner = models.CharField(max_length = 64, default = None, blank = True, null = True)
    category = models.CharField(max_length = 64)
    starting_bid = models.IntegerField()
    current_bid = models.IntegerField(default = None)
    img_url = models.URLField(max_length = 300, default = None, blank = True, null = True)
    active = models.BooleanField(default = True)

class WatchList(models.Model):
    watcher = models.CharField(max_length = 64)
    list_id = models.IntegerField()

class Bids(models.Model):
    bid = models.IntegerField()
    list_id = models.IntegerField()
    user = models.CharField(max_length = 64)

class Comments(models.Model):
    comment = models.CharField(max_length = 500)
    list_id = models.IntegerField()
    user = models.CharField(max_length = 64)
    posting_time = models.CharField(max_length = 64)

class Categories(models.Model):
    category = models.CharField(max_length = 64)
