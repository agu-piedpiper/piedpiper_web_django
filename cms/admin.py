from django.contrib import admin
from cms.models import Category, Activity, Techcategory, Techblog


# Register your models here.


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status')
    list_display_links = ('id', 'title')


class TechblogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status')
    list_display_links = ('id', 'title')


class TechblogInline(admin.TabularInline):
    model = Techblog.categories.through


class TechcategoryAdmin(admin.ModelAdmin):
    inlines = [TechblogInline]


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Category)
admin.site.register(Techblog, TechblogAdmin)
admin.site.register(Techcategory, TechcategoryAdmin)