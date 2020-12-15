from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from cms.note import Note,Image
from cms.models import Article
from cms.forms import ArticleForm

import re


def article_list(request):
    # 記事の一覧
    # return HttpResponse('記事の一覧')
    articles = Article.objects.all().order_by('id')

    return render(request,'cms/article_list.html',{'articles':articles})



def article_edit(request, article_id=None):
    # 記事の編集
    if article_id:   # article_id が指定されている (修正時)
        article = get_object_or_404(Article, pk=article_id)
    else:         # article_id が指定されていない (追加時)
        article = Article()
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)  # POST された request データからフォームを作成
        if form.is_valid():    # フォームのバリデーション
            article = form.save(commit=False)
            article.image = request.FILES['image']
            article.save()
            return redirect('cms:article_list')
    else:    # GET の時
        form = ArticleForm(instance=article)  # article インスタンスからフォームを作成

    return render(request, 'cms/article_edit.html', dict(form=form, article_id=article_id))


def article_del(request, article_id):
    # 記事の削除
    article = get_object_or_404(Article, pk=article_id)
    article.delete()
    return redirect('cms:article_list')

# 'title', 'body', 'image','categories','published_at','updated_at','note','status'
def note_add(request):
    note = Note()
    note_list = note.get_deta()
    registered_note_key = Article.objects.exclude(note_key = None).values_list('note_key', flat=True)
    for n in note_list:
        note_key = n["key"]
    # note_key = "ne40b6a301258"
        if note_key not in registered_note_key:
            note_article=note.get_note(note_key)
            article = Article()
            article.title=note_article['name']
            article.body=Image.rewriting_img_path(note_article['body'],note_article['key'])
            # article.body=note_article['body']
            article.note_key=note_article['key']
            # article.image=note_article['eyecatch']
            article.note=2

            article.save()
    return redirect('cms:article_list')
     

