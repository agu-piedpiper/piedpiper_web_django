from django.forms import ModelForm
from cms.models import Activity, Techblog


class ActivityForm(ModelForm):
    """記事のフォーム"""
    class Meta:
        model = Activity
        fields = ('title', 'body', 'image', 'categories', 'status')


class TechblogForm(ModelForm):
    """記事のフォーム"""
    class Meta:
        model = Techblog
        fields = ('title', 'body', 'image', 'categories', 'status')