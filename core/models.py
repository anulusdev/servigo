from django.db import models
from django_fsm import transition, FSMField


class Status(models.TextChoices):
    OPEN = 'Open', 'open'
    FULL = 'Full', 'full'
    COMPLETE = 'Complete', 'complete'


class Faculty(models.TextChoices):
    Saat = 'SAAT', 'SAAT'
    Sbms = 'SBMS', 'SBMS'
    Sems = 'SEMS', 'SEMS'
    Sese = 'SESE', 'SESE'
    Set = 'SET', 'SET'
    Simme = 'SIMME', 'SIMME'
    Slit = 'SLIT', 'SLIT'
    Sls = 'SLS', 'SLS'
    Soc = 'SOC', 'SOC'
    Sps = 'SPS', 'SPS'
        
    
class Trip(models.Model):

    status = FSMField(choices=Status.choices, default=Status.OPEN, protected=True)

    @transition(field=status, source=Status.OPEN, target=Status.FULL)
    def mark_full(self):
        pass

    @transition(field=status, source=Status.FULL, target=Status.COMPLETE)
    def mark_complete(self):
        pass


class Location(models.Model):
        
    name = models.CharField(max_length=50)
    capacity = models.IntegerField(default=3)
    trip = models.ForeignKey(Trip, null=False, blank=False, on_delete=models.CASCADE, related_name='locations')
    faculty = models.CharField(max_length=10, choices=Faculty.choices, default=Faculty.Saat)
