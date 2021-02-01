from django.shortcuts import render
from cms.models import Activity,Techblog
import re
# Create your views here.
def index(request):
    activities = Activity.objects.all().order_by('id')[0:3]
    p = re.compile(r"<[^>]*?>")
    for activity in activities:
        activity.body = activity.body.replace("　", "").replace("\n", "")
        activity.body =p.sub("", activity.body)
       
        activity.published_at = activity.published_at.strftime("%Y/%m/%d")
       
    return render(request, 'website/index.html',{'activities': activities})

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