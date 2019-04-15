from django.urls import path
from . import views

app_name = 'core'
urlpatterns =  [
   path('', views.index, name='index'),
   path('create/',views.createProject,name='createProject'),
   path('<int:project_id>/',views.detail,name='detail'),
   path('<int:project_id>/timing/',views.starttiming,name='starttiming'),
   path('<int:project_id>/stoptiming/',views.stoptiming,name='stoptiming'),
]
