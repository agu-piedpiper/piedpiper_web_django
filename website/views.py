from django.shortcuts import render
from cms.models import Activity,Techblog
import re
# Create your views here.
def index(request):
    activities = Activity.objects.all().order_by('id')[0:3]
    techblogs = Techblog.objects.all().order_by('id')[0:3]
    p = re.compile(r"<[^>]*?>")
    for activity in activities:
        activity.body = activity.body.replace("　", "").replace("\n", "")
        activity.body =p.sub("", activity.body)
        activity.published_at = activity.published_at.strftime("%Y/%m/%d")

    for techblog in techblogs:
        techblog.body = techblog.body.replace("　", "").replace("\n", "")
        techblog.body =p.sub("", techblog.body)
        techblog.published_at = techblog.published_at.strftime("%Y/%m/%d")
       
    return render(request, 'website/index.html',{'activities': activities,'techblogs':techblogs})

def activity_list(request):
    activities = Activity.objects.all().order_by('id')
    p = re.compile(r"<[^>]*?>")
    for activity in activities:
        activity.body = activity.body.replace("　", "").replace("\n", "")
        activity.body =p.sub("", activity.body)
        activity.published_at = activity.published_at.strftime("%Y/%m/%d")
       
    return render(request, 'website/activity.html',{'activities': activities})

def activity_detail(request,request_id):    
    activity = Activity.objects.get(id=request_id)
    return render(request, 'website/activity_detail.html',{'activity': activity})

def techblog_list(request):
    techblogs = Techblog.objects.all().order_by('id')
    p = re.compile(r"<[^>]*?>")
    for techblog in techblogs:
        techblog.body = techblog.body.replace("　", "").replace("\n", "")
        techblog.body =p.sub("", techblog.body)
        techblog.published_at = techblog.published_at.strftime("%Y/%m/%d")
       
    return render(request, 'website/techblog.html',{'techblogs':techblogs})

def techblog_detail(request,request_id):    
    techblog =Techblog.objects.get(id=request_id)
    return render(request, 'website/techblog_detail.html',{'techblog': techblog})