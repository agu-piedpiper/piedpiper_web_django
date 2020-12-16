from django.forms import ModelForm
from cms.models import Activity


class ActivityForm(ModelForm):
    """記事のフォーム"""
    class Meta:
        model = Activity
        fields = ('title', 'body', 'image','categories','status' ) 
       