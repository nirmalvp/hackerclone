from django.shortcuts import render
from news.models import Article
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

def index(request):
    articles_list = Article.objects.annotate(
            article_upvotes=Count('vote')).order_by("-article_addeddate")
    paginator = Paginator(articles_list, 3) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)
    return render(request, 'news/index.html', {"articles": articles})

def contact(request):
    return render(request,'news/contact.html')

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

