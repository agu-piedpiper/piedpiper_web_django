from django.urls import path
from . import views
app_name = 'cms'
urlpatterns = [
    path('activiy/', views.activiy_list, name='activiy_list'),   # 一覧
    path('activiy/add/', views.activiy_edit, name='activiy_add'),  # 登録
    path('activiy/note_add/', views.note_add, name='note_add'),  # 追加
    path('activiy/mod/<int:activiy_id>/', views.activiy_edit, name='activiy_mod'),  # 修正
    path('activiy/del/<int:activiy_id>/', views.activiy_del, name='activiy_del'),   # 削除
]