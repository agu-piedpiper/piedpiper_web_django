# Generated by Django 3.1.4 on 2021-01-29 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='techblog',
            old_name='note_item_id',
            new_name='qiita_item_id',
        ),
        migrations.RemoveField(
            model_name='techblog',
            name='note',
        ),
        migrations.AddField(
            model_name='techblog',
            name='qiita',
            field=models.PositiveSmallIntegerField(default=1, help_text='1:直接投稿, 2:Qiita転載', verbose_name='Qiita転載'),
        ),
    ]
