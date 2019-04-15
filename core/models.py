from django.db import models
from django.utils import timezone

# Create your models here.

class Project(models.Model):
   project_name = models.CharField(max_length=200)
   pub_date = models.DateTimeField('date created')
   active_timeentry_id = models.IntegerField(default=0)
   def __str__(self):
      return self.project_name

   def cleanup(self):
       timeentries = self.timeentry_set.all()
       for timeentry in timeentries:
           if timeentry.delta_minutes < 1:
               timeentry.delete()



class TimeEntry(models.Model):
    #TODO: Remove all timeentries with delta smaller than 1 min
   project = models.ForeignKey(Project, on_delete=models.CASCADE)
   start_time = models.DateTimeField(default=timezone.now())
   stop_time = models.DateTimeField(default=timezone.now())
   delta_minutes = models.IntegerField(default=0) # delta time in minutes

   def __str__(self):
      return str(self.start_time)

   def calculate_Delta_Time(self):
       if self.stop_time <= self.start_time:
           self.delta_minutes = 0
       delta_time = self.stop_time - self.start_time
       self.delta_minutes = delta_time.seconds//60
