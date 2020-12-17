from django.urls import path
from . import views
app_name = 'cms'
urlpatterns = [
    path('activiy/', views.activiy_list, name='activiy_list'),   # 一覧
    path('activiy/add/', views.activiy_edit, name='activiy_add'),  # 登録
    path('activiy/note_add/', views.note_add, name='note_add'),  # 追加
    path('activiy/mod/<int:activiy_id>/', views.activiy_edit, name='activiy_mod'),  # 修正
    path('activiy/del/<int:activiy_id>/', views.activiy_del, name='activiy_del'),   # 削除

    path('techblog/', views.techblog_list, name='techblog_list'),   # 一覧
    path('techblog/add/', views.techblog_edit, name='techblog_add'),  # 登録
    path('techblog/note_add/', views.note_add, name='note_add'),  # 追加
    path('techblog/mod/<int:techblog_id>/', views.techblog_edit, name='techblog_mod'),  # 修正
    path('techblog/del/<int:techblog_id>/', views.techblog_del, name='techblog_del'),   # 削除
]