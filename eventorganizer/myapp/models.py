from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class Department(models.Model):
    
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('participant', 'Participant'),
        ('organizer', 'Organizer'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    department = models.ForeignKey("Department", on_delete=models.SET_NULL, null=True)

    def is_participant(self):
        return self.role == 'participant'

    def is_organizer(self):
        return self.role == 'organizer'
    
class Venue(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField()
    
    def __str__(self):
        return self.name
    

class Event(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('disapproved', 'Disapproved'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(default=now,null=False,blank=False)
    venue = models.ForeignKey(Venue,on_delete=models.SET_NULL, null=True, blank=True)
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    department = models.ManyToManyField("Department", blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    certificate_template = models.ImageField(upload_to="certificate_templates",null=True,blank=True)
    notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"
    
class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')], blank=True, null=True)
    certificate = models.ImageField(upload_to="certificates/", blank=True, null=True)

    def __str__(self):
        return self.participant.username
    
    def is_attended(self):
        return self.status == "Present"
    

    

    
    