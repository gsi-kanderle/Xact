from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from .models import Project, TimeEntry

def create_detail_context(project):
    latest_timeentries = project.timeentry_set.order_by('-start_time')[:5]
    context = {
        'latest_timeentries': latest_timeentries,
        'project': project,
        }
    return context

def stop_project_timing(project):
    active_id = project.active_timeentry_id
    if active_id == 0:
        return False
    t = get_object_or_404(TimeEntry, pk=active_id)
    t.stop_time = timezone.now()
    t.calculate_Delta_Time()
    if t.delta_minutes < 1:
        t.delete()
    else:
        t.save()
    project.active_timeentry_id = 0
    project.save()
    return True

def stop_active_projects(current_project):
    projects = Project.objects.all()
    for p in projects:
        if p.id == current_project.id:
            continue
        if not stop_project_timing(p):
            continue


def index(request):
    latest_project_list = Project.objects.order_by('-pub_date')[:5]
    context = {
        'latest_project_list':  latest_project_list
    }
    return render(request, 'index.html', context = context)

def detail(request, project_id):
    p = get_object_or_404(Project, pk=project_id)
    context = create_detail_context(p)
    return render(request, 'detail.html', context = context)

def starttiming(request, project_id):
    p = get_object_or_404(Project, pk=project_id)
    active_id = p.active_timeentry_id
    if active_id > 0:
        return HttpResponse("Error, can't time with existing active id: " + str(active_id))
    t = p.timeentry_set.create(start_time=timezone.now())
    t.save()
    p.active_timeentry_id = t.id
    p.save()
    stop_active_projects(p)
    context = create_detail_context(p)
    return render(request, 'detail.html', context = context)

def stoptiming(request, project_id):
    p = get_object_or_404(Project, pk=project_id)
    if not stop_project_timing(p):
        return HttpResponse("Error, no active id: " + str(active_id))
    context = create_detail_context(p)
    return render(request, 'detail.html', context = context)

def results(request, project_id):
    Project = get_object_or_404(Project, pk=project_id)
    return render(request, 'core/results.html', {'Project': Project})

def createProject(request):
    name = request.POST['Project Name']
    try:
        p = Project.objects.get(project_name=name)
    except:
        p = Project(project_name=name,pub_date=timezone.now(),active_timeentry_id=0)
        p.save()
        return HttpResponseRedirect("Created: " + name + " with ID: " + str(p.id))
    return HttpResponse(name + " already exist")
