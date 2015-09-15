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
import functools
import warnings

from django.conf import settings
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.utils.deprecation import (
    RemovedInDjango20Warning, RemovedInDjango110Warning,
)
from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.six.moves.urllib.parse import urlparse, urlunparse
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

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
    print "isndi"
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


# @sensitive_post_parameters()
# @csrf_protect
# @never_cache
# def login(request, template_name='registration/login.html',
#           redirect_field_name='/',
#           authentication_form=AuthenticationForm,
#           extra_context=None):
#     """
#     Displays the login form and handles the login action.
#     """

#     redirect_to = request.POST.get(redirect_field_name,
#                                    request.GET.get(redirect_field_name, ''))

#     if request.method == "POST":

#         form = authentication_form(request, data=request.POST)
#         if form.is_valid():
#             print "Vlid"

#             # Ensure the user-originating redirection url is safe.
#             if not is_safe_url(url=redirect_to, host=request.get_host()):
#                 redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

#             # Okay, security check complete. Log the user in.
#             auth_login(request, form.get_user())

#             return HttpResponseRedirect(redirect_to)
#     else:

#         form = authentication_form(request)

#     current_site = get_current_site(request)
#     print vars(form)
#     context = {
#         'form': form,
#         redirect_field_name: redirect_to,
#         'site': current_site,
#         'site_name': current_site.name,
#     }
#     if extra_context is not None:
#         context.update(extra_context)

#     return TemplateResponse(request, template_name, context)


