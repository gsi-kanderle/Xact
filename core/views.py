from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from .models import Project, TimeEntry

def index(request):
    latest_project_list = Project.objects.order_by('-pub_date')[:5]
    context = {
        'latest_project_list':  latest_project_list
    }
    return render(request, 'index.html', context = context)

def detail(request, project_id):
    p = get_object_or_404(Project, pk=project_id)
    #latest_timeentries = Project.timeentry_set.order_by('-start_time')[:5]
    context = {
        'latest_timeentries': None,
        'project': p,
        'stop': True
    }
    return render(request, 'detail.html', context = context)

def starttiming(request, project_id):
    p = get_object_or_404(Project, pk=project_id)
    t = p.timeentry_set.create(start_time=timezone.now())
    latest_timeentries = Project.timeentry_set.order_by('-start_time')[:5]
    context = {
        'latest_timeentries': None,
        'Project': p,
        'stop': False,
        'timeentry': t,
    }
    return render(request, 'detail.html', context = context)

def stoptiming(request, project_id, timeentry_id):
    p = get_object_or_404(Project, pk=project_id)
    t = get_object_or_404(TimeEntry, pk=timeentry_id)
    t.stop_time = timezone.now()
    t.calculate_Delta_Time()
    latest_timeentries = Project.timeentry_set.order_by('-start_time')[:5]
    context = {
        'latest_timeentries': None,
        'Project': p,
        'stop': True,
        'timeentry': t,
    }
    return render(request, 'detail.html', context = context)

def results(request, project_id):
    Project = get_object_or_404(Project, pk=project_id)
    return render(request, 'core/results.html', {'Project': Project})

def createProject(request):
    name = request.POST['Project Name']
    try:
        p = Project.objects.get(project_name=name)
    except:
        p = Project(project_name=name,pub_date=timezone.now())
        p.save()
        return HttpResponseRedirect("Created: " + name + " with ID: " + str(p.id))
    return HttpResponse(name + " already exist")
