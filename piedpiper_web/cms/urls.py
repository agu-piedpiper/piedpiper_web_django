from django.urls import path
from . import views
app_name = 'cms'
urlpatterns = [
    path('article/', views.article_list, name='article_list'),   # 一覧
    path('article/add/', views.article_edit, name='article_add'),  # 登録
    path('article/note_add/', views.note_add, name='note_add'),  # 追加
    path('article/mod/<int:article_id>/', views.article_edit, name='article_mod'),  # 修正
    path('article/del/<int:article_id>/', views.article_del, name='article_del'),   # 削除
]