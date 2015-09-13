from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    user = models.ForeignKey(User)
    article_title = models.CharField(max_length=200)
    article_url = models.CharField(max_length=200)
    article_upvotes= models.IntegerField(default=0)
    article_addeddate = models.DateTimeField(auto_now=True)
