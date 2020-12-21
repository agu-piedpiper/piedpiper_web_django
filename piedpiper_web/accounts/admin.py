from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Campus,Undergraduate,Departments
 
 
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('student_number','campus','undergraduate','department','year')}),)
    list_display = ['username', 'email', 'year']
 
 
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Campus)
admin.site.register(Undergraduate)
admin.site.register(Departments)