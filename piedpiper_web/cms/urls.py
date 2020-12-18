from django.urls import path
from . import views
app_name = 'cms'
urlpatterns = [
    path('activity/', views.activity_list, name='activity_list'),   # 一覧
    path('activity/add/', views.activity_edit, name='activity_add'),  # 登録
    path('activity/note_add/', views.note_add, name='note_add'),  # 追加
    path('activity/mod/<int:activity_id>/', views.activity_edit, name='activity_mod'),  # 修正
    path('activity/del/<int:activity_id>/', views.activity_del, name='activity_del'),   # 削除

    path('techblog/', views.techblog_list, name='techblog_list'),   # 一覧
    path('techblog/add/', views.techblog_edit, name='techblog_add'),  # 登録
    path('techblog/note_add/', views.note_add, name='note_add'),  # 追加
    path('techblog/mod/<int:techblog_id>/', views.techblog_edit, name='techblog_mod'),  # 修正
    path('techblog/del/<int:techblog_id>/', views.techblog_del, name='techblog_del'),   # 削除
]