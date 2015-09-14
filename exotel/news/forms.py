from news.models import Article
from django import forms
import requests

class ArticleForm(forms.ModelForm):
    class Meta():
        model = Article
        fields = ("article_url", )
    def clean_article_url(self):
        article_url = self.cleaned_data["article_url"]
        if not requests.get(article_url).ok :
            raise forms.ValidationError("The page mentioned doesn't exist")
        return article_url


