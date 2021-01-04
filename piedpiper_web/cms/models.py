from django.db import models
from django.utils import timezone
from accounts.models import CustomUser


# Create your models here.

class Category(models.Model):
    name = models.CharField("カテゴリ名", max_length=31)
    
    class Meta:
        verbose_name_plural = "活動カテゴリ"
    
    def __str__(self):
        return self.name


class Techcategory(models.Model):
    name = models.CharField("カテゴリ名", max_length=31)

    class Meta:
        verbose_name_plural = "技術カテゴリ"

    def __str__(self):
        return self.name


class Activity(models.Model):
    # 活動記事
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("タイトル", max_length=255)
    body = models.TextField("本文")
    image = models.ImageField("画像", upload_to='images/', null=True, blank=True)
    categories = models.ManyToManyField(Category, "カテゴリ")
    published_at = models.DateTimeField("公開日", default=timezone.now)
    updated_at = models.DateTimeField("更新日", default=timezone.now)
    is_note = models.BooleanField("Note転載", default=False)
    note_item_id = models.CharField("noteキー", max_length=255, null=True, blank=True)
    status = models.BooleanField("公開ステータス", default=False)
    
    class Meta:
        verbose_name_plural = "Activity(活動記事)"
    
    def __str__(self):
        return self.title


class Techblog(models.Model):
    # プログラミング
    
    title = models.CharField("タイトル", max_length=255)
    body = models.TextField("本文")
    image = models.ImageField("画像", upload_to='images/', null=True, blank=True)
    categories = models.ManyToManyField(Techcategory, "カテゴリ")
    published_at = models.DateTimeField("公開日", default=timezone.now)
    updated_at = models.DateTimeField("更新日", default=timezone.now)
    is_qiita = models.BooleanField("Qiita転載", default=False)
    qiita_item_id = models.CharField("Qiita_投稿ID", max_length=30)
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True,
                                    related_name="techblog_custom_user", verbose_name="投稿ユーザID")
    status = models.BooleanField("公開ステータス", default=False)
    
    class Meta:
        verbose_name_plural = "Techblog(技術記事)"
    
    def __str__(self):
        return self.title
