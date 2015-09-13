from django.shortcuts import render
from news.models import Article
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    articles_list = Article.objects.order_by("-article_addeddate")
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

