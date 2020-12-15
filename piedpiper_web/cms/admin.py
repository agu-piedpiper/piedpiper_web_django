from django.contrib import admin
from cms.models import Category,Article
# Register your models here.
admin.site.register(Category)


class ArticleAdmin(admin.ModelAdmin):
    list_display=('id','title','status')
    list_display_links = ('id','title') 

admin.site.register(Article,ArticleAdmin)