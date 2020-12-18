from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from cms.note import Note, Image
from cms.models import Activity,Techblog
from cms.forms import ActivityForm,TechblogForm

import re


# -------------------------------Activity
def activity_list(request):
    # 記事の一覧
    # return HttpResponse('記事の一覧')
    activities = Activity.objects.all().order_by('id')

    return render(request, 'cms/activity_list.html', {'activities': activities})


def activity_edit(request, activity_id=None):
    # 記事の編集
    if activity_id:   # activity_id が指定されている (修正時)
        activity = get_object_or_404(Activity, pk=activity_id)
    else:         # activity_id が指定されていない (追加時)
        activity = Activity()
    if request.method == 'POST':
        # POST された request データからフォームを作成
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():    # フォームのバリデーション
            activity = form.save(commit=False)
            activity.image = request.FILES['image']
            activity.save()
            return redirect('cms:activity_list')
    else:    # GET の時
        form = ActivityForm(instance=activity)  # activity インスタンスからフォームを作成

    return render(request, 'cms/activity_edit.html', dict(form=form, activity_id=activity_id))


def activity_del(request, activity_id):
    # 記事の削除
    activity = get_object_or_404(Activity, pk=activity_id)
    activity.delete()
    return redirect('cms:activity_list')




def note_add(request):
    note = Note()
    note_list = note.get_deta()
    registered_note_key = Activity.objects.exclude(
        note_key=None).values_list('note_key', flat=True)
    for n in note_list:
        note_key = n["key"]
    # note_key = "ne40b6a301258"
        if note_key not in registered_note_key:
            note_activity = note.get_note(note_key)
            activity = Activity()
            activity.title = note_activity['name']
            activity.body = Image.rewriting_img_path(
                note_activity['body'], note_activity['key'])
            activity.note_key = note_activity['key']

            activity.image = Image.rename_eyecatch(
                note_activity['eyecatch'], note_activity['key'])
            activity.note = 2

            activity.save()
    return redirect('cms:activity_list')


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