from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from cms.note import Note, Image
from cms.models import Activity,Techblog
from cms.forms import ActivityForm,TechblogForm

import re


# -------------------------------Activity
def activiy_list(request):
    # 記事の一覧
    # return HttpResponse('記事の一覧')
    activities = Activity.objects.all().order_by('id')

    return render(request, 'cms/activiy_list.html', {'activities': activities})


def activiy_edit(request, activiy_id=None):
    # 記事の編集
    if activiy_id:   # activiy_id が指定されている (修正時)
        activiy = get_object_or_404(Activity, pk=activiy_id)
    else:         # activiy_id が指定されていない (追加時)
        activiy = Activity()
    if request.method == 'POST':
        # POST された request データからフォームを作成
        form = ActivityForm(request.POST, instance=activiy)
        if form.is_valid():    # フォームのバリデーション
            activiy = form.save(commit=False)
            activiy.image = request.FILES['image']
            activiy.save()
            return redirect('cms:activiy_list')
    else:    # GET の時
        form = ActivityForm(instance=activiy)  # activiy インスタンスからフォームを作成

    return render(request, 'cms/activiy_edit.html', dict(form=form, activiy_id=activiy_id))


def activiy_del(request, activiy_id):
    # 記事の削除
    activiy = get_object_or_404(Activity, pk=activiy_id)
    activiy.delete()
    return redirect('cms:activiy_list')




def note_add(request):
    note = Note()
    note_list = note.get_deta()
    registered_note_key = Activity.objects.exclude(
        note_key=None).values_list('note_key', flat=True)
    for n in note_list:
        note_key = n["key"]
    # note_key = "ne40b6a301258"
        if note_key not in registered_note_key:
            note_activiy = note.get_note(note_key)
            activiy = Activity()
            activiy.title = note_activiy['name']
            activiy.body = Image.rewriting_img_path(
                note_activiy['body'], note_activiy['key'])
            activiy.note_key = note_activiy['key']

            activiy.image = Image.rename_eyecatch(
                note_activiy['eyecatch'], note_activiy['key'])
            activiy.note = 2

            activiy.save()
    return redirect('cms:activiy_list')


# -------------------------------techblog
def techblog_list(request):

    techblogs = Techblog.objects.all().order_by('id')

    return render(request, 'cms/techblog_list.html', {'techblogs': techblogs})


def techblog_edit(request, techblog_id=None):
    # 記事の編集
    if techblog_id:   # techblog_id が指定されている (修正時)
        techblog = get_object_or_404(Techblog, pk=techblog_id)
    else:         # techblog_id が指定されていない (追加時)
        techblog = Techblog()
    if request.method == 'POST':
        # POST された request データからフォームを作成
        form = TechblogForm(request.POST, instance=techblog)
        if form.is_valid():    # フォームのバリデーション
            techblog = form.save(commit=False)
            techblog.image = request.FILES['image']
            techblog.save()
            return redirect('cms:techblog_list')
    else:    # GET の時
        form = TechblogForm(instance=techblog)  # techblog インスタンスからフォームを作成

    return render(request, 'cms/techblog_edit.html', dict(form=form, techblog_id=techblog_id))


def techblog_del(request, techblog_id):
    # 記事の削除
    techblog = get_object_or_404(Techblog, pk=techblog_id)
    techblog.delete()
    return redirect('cms:techblog_list')