from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from cms.note import Note,Image
from cms.models import Activity
from cms.forms import ActivityForm

import re


def activiy_list(request):
    # 記事の一覧
    # return HttpResponse('記事の一覧')
    activities = Activity.objects.all().order_by('id')

    return render(request,'cms/activiy_list.html',{'activities':activities})



def activiy_edit(request, activiy_id=None):
    # 記事の編集
    if activiy_id:   # activiy_id が指定されている (修正時)
        activiy = get_object_or_404(Activity, pk=activiy_id)
    else:         # activiy_id が指定されていない (追加時)
        activiy = Activity()
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activiy)  # POST された request データからフォームを作成
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

# 'title', 'body', 'image','categories','published_at','updated_at','note','status'
def note_add(request):
    note = Note()
    note_list = note.get_deta()
    registered_note_key = Activity.objects.exclude(note_key = None).values_list('note_key', flat=True)
    for n in note_list:
        note_key = n["key"]
    # note_key = "ne40b6a301258"
        if note_key not in registered_note_key:
            note_activiy=note.get_note(note_key)
            activiy = Activity()
            activiy.title=note_activiy['name']
            activiy.body=Image.rewriting_img_path(note_activiy['body'],note_activiy['key'])
            # activiy.body=note_activiy['body']
            activiy.note_key=note_activiy['key']

            # dst_path=f'./media/images/{image_name}.{img_extension}'
            # eyecatch_img_name=f'top_{activiy.note_key}'
            # Image.download_img(note_activiy['eyecatch'],new_path)
            # activiy.image=Image.rewriting_img_path(note_activiy['eyecatch'],eyecatch_img)
            print(note_activiy['eyecatch'])
            # https://assets.st-note.com/production/uploads/images/12066309/rectangle_large_type_2_3f83616f0ad914bbf0d5ce0411fa478c.jpeg?fit=bounds&quality=60&width=1280
            activiy.note=2

            activiy.save()
    return redirect('cms:activiy_list')
     

