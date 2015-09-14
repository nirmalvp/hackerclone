from django.shortcuts import render
from news.models import Article,Vote
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from news.forms import ArticleForm
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
import json

def index(request):
    articles_list = Article.objects.annotate(
            article_upvotes=Count('vote')).order_by("-article_addeddate")
    paginator = Paginator(articles_list, 3) # Show 25 contacts per page
    page = request.GET.get('page')
    voted = []
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)
    if request.user.is_authenticated():
        voted = Vote.objects.filter(voter=request.user)
        articles_in_page = [article.id for article in articles]
        voted = voted.filter(article_id__in=articles_in_page)
        voted = [vote.article_id for vote in voted]
    return render(request, 'news/index.html', {"articles": articles, "voted":voted})


@login_required
def submit(request):
    if request.method =='POST':
        article_title = request.POST['linktitle']
        article_url = request.POST['linkurl']
        article_user = request.user
        Article.objects.create(article_title = article_title, article_url = article_url,
            user = article_user)
        return HttpResponseRedirect('/') # Redirect after POST
    return render(request,'news/submit.html')

def gettitle(request):
    if request.method =='POST':
        response_data={}
        response_data['error'] = False
        linkurl = request.POST['link']
        try:
            r = requests.get(linkurl,timeout = 15)
        except:
            response_data['error'] = True
            return HttpResponse(json.dumps(response_data),content_type="application/json")
        else:
            soup = BeautifulSoup(r.text)
            response_data['pageTitle'] = soup.title.string
            return HttpResponse(json.dumps(response_data),content_type="application/json")
    return HttpResponseRedirect('/')


def register(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            return HttpResponseRedirect('/') # Redirect after POST
    else:
        form = UserCreationForm() # An unbound form
    return render(request,'registration/register.html', {'form': form})


def upvote(request):

    if request.method =='POST':

        articleId = request.POST["articleId"]
        print articleId
        response_data = {}
        response_data['error'] = False
        article = Article.objects.get(pk=articleId)
        totalVotes = article.vote_set.count()
        user = request.user

        if not user.is_authenticated():
            response_data['error'] = True
            return HttpResponse(json.dumps(response_data),content_type="application/json")
        previousVotes = Vote.objects.filter(voter=user, article=article)
        hasVoted = (previousVotes.count() != 0)
        if not hasVoted:
            v = Vote.objects.create(voter= user,article = article)
            totalVotes += 1
            response_data['btn_text'] = "Upvoted"

        else :
            previousVotes[0].delete()
            totalVotes -= 1
            response_data['btn_text'] = "Upvote"
        response_data['total_votes'] = totalVotes
    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json")


