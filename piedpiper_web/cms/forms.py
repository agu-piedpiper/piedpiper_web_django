from django.forms import ModelForm
from cms.models import Article


class ArticleForm(ModelForm):
    """記事のフォーム"""
    class Meta:
        model = Article
        fields = ('title', 'body', 'image','categories','status' ) 
       