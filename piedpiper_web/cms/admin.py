from django.contrib import admin
from cms.models import Category,Activity,Techcategory,Techblog
# Register your models here.



class ActivityAdmin(admin.ModelAdmin):
    list_display=('id','title','status')
    list_display_links = ('id','title') 




class TechblogAdmin(admin.ModelAdmin):
    list_display=('id','title','status')
    list_display_links = ('id','title')


admin.site.register(Category)
admin.site.register(Techcategory)
admin.site.register(Activity,ActivityAdmin)
admin.site.register(Techblog,TechblogAdmin)
