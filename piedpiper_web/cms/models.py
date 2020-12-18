from django.db import models
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField("カテゴリ名",max_length=31,)
    class Meta:

        verbose_name_plural = "活動カテゴリ"

    def __str__(self):
        return self.name

class Techcategory(models.Model):
    name = models.CharField("カテゴリ名",max_length=31,)
    class Meta:

        verbose_name_plural = "技術カテゴリ"

    def __str__(self):
        return self.name


class Activity(models.Model):
    # 活動記事
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("タイトル",max_length=255)
    body = models.TextField("本文")
    image = models.ImageField("画像",upload_to='images/',null=True, blank=True)
    categories = models.ManyToManyField(Category,"カテゴリ")
    published_at = models.DateTimeField("公開日",default=timezone.now)
    updated_at = models.DateTimeField("更新日",default=timezone.now)
    note = models.PositiveSmallIntegerField("Note転載",default=1, help_text="1:直接投稿, 2:note転載")
    note_key = models.CharField("noteキー",max_length=255,null=True, blank=True)
    status = models.PositiveSmallIntegerField("公開ステータス",default=1, help_text="1:下書き, 2:公開")

    class Meta:

        verbose_name_plural = "Activity(活動記事)"

    def __str__(self):
        return self.title

class Techblog(models.Model):
    # プログラミング
    
    title = models.CharField("タイトル",max_length=255)
    body = models.TextField("本文")
    image = models.ImageField("画像",upload_to='images/',null=True, blank=True)
    categories = models.ManyToManyField(Techcategory,"カテゴリ")
    published_at = models.DateTimeField("公開日",default=timezone.now)
    updated_at = models.DateTimeField("更新日",default=timezone.now)
    note = models.PositiveSmallIntegerField("Qiita転載",default=1, help_text="1:直接投稿, 2:note転載")
    note_key = models.CharField("Qiitaキー",max_length=255,null=True, blank=True)
    status = models.PositiveSmallIntegerField("公開ステータス",default=1, help_text="1:下書き, 2:公開")

    class Meta:

        verbose_name_plural = "Techblog(技術記事)"

    def __str__(self):
        return self.title

