from django.db import models
from django.utils import timezone

# Create your models here.

class Project(models.Model):
   project_name = models.CharField(max_length=200)
   pub_date = models.DateTimeField('date created')

   def __str__(self):
      return self.project_name

   def was_published_recently(self):
      return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class TimeEntry(models.Model):
   project = models.ForeignKey(Project, on_delete=models.CASCADE)
   start_time = models.DateTimeField()
   stop_time = models.DateTimeField()
   delta_time = models.DateTimeField()

   def __str__(self):
      return self.start_time

   def calculate_Delta_Time(self):
       if self.stop_time == self.start_time:
           self.delta_time = None
       if self.stop_time < self.start_time:
           self.delta_time = None
       self.delta_time = self.stop_time.timedelta(self.start_time)
