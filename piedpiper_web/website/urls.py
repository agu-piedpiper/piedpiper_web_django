from django.urls import path
from . import views
app_name = 'website'
urlpatterns = [
    path('', views.index, name='index'), 
    path('activity/', views.activity_list, name='activity_list'), 
    path('activity/<int:request_id>/', views.activity_detail, name='activity_detail'), 
]