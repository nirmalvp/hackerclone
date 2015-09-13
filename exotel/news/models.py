from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

class LinkVoteCountManager(models.Manager):
    def get_query_set(self):
        return super(LinkVoteCountManager, self).get_query_set().annotate(
            votes=Count('vote')).order_by('-votes')

class Article(models.Model):
    objects = models.Manager()
    with_vote = LinkVoteCountManager()
    article_title = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    article_addeddate = models.DateTimeField(auto_now_add=True)
    article_url = models.URLField("URL", max_length=250, blank=True)
    def __unicode__(self):
        return self.article_title

class Vote(models.Model):
    voter = models.ForeignKey(User)
    article = models.ForeignKey(Article)

    def __unicode__(self):
        return "%s upvoted %s" % (self.voter.username, self.article.article_title)
