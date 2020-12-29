from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Campus(models.Model):
    name = models.CharField("キャンパス",max_length=31,)
    class Meta:
        verbose_name_plural = "キャンパス"
    def __str__(self):
        return self.name

class Undergraduate(models.Model):
    name = models.CharField("学部",max_length=31,)
    class Meta:
        verbose_name_plural = "学部"
    def __str__(self):
        return self.name


class Departments(models.Model):
    name = models.CharField("学科",max_length=31,)
    class Meta:
        verbose_name_plural = "学科"
    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    qiita_user_id = models.CharField("Qiita_ユーザーID",max_length=30, null=True, blank=True)
    campus = models.ManyToManyField(Campus,"キャンパス")
    undergraduate = models.ManyToManyField(Undergraduate,"学部")
    department = models.ManyToManyField(Departments,"学科")
    year = models.PositiveSmallIntegerField("学年",validators=[MinValueValidator(1), MaxValueValidator(5)],null=True)
    language = models.CharField("プログラミング言語",max_length=255,null=True)
