from django.urls import path
from . import views
app_name = 'accounts'

urlpatterns = [
    
    path('login/', views.login, name='login'  namespace='login'), 
    path('logout/', views.logout, name='logout'), 
    ]
