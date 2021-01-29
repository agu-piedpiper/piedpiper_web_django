from django.urls import path
from . import views
app_name = 'website'
urlpatterns = [
    path('', views.index, name='index'), 
    path('activity/', views.activity_list, name='activity_list'), 
    path('activity/<int:request_id>/', views.activity_detail, name='activity_detail'), 
    path('techblog/', views.techblog_list, name='techblog_list'), 
    path('techblog/<int:request_id>/', views.techblog_detail, name='techblog_detail'), 
]