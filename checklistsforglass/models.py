from django.db import models
from django.contrib.auth.models import User

class Checklist(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(User)
    description = models.TextField(blank=True)
    video_url = models.CharField(max_length=300, blank=True)
    


    def __unicode__(self):
        return '%s by %s' % (self.name, self.author.username)

    def get_elements(self):
        return [{'text': i.text, 'image': i.image.url} if i.image else {'text': i.text, 'image': ''} for i in ChecklistElement.objects.filter(checklist=self).order_by('order')]

    def delete_elements(self):
        [i.delete() for i in ChecklistElement.objects.filter(checklist=self)]

class ChecklistV2(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(User)
    description = models.TextField(blank=True)
    video_url = models.CharField(max_length=300, blank=True)
    json = models.TextField(blank=True)


    def __unicode__(self):
        return '%s by %s' % (self.name, self.author.username)


class ChecklistElement(models.Model):
    checklist = models.ForeignKey(Checklist)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='elements/', blank=True)
    order = models.PositiveIntegerField()
 
    def __unicode__(self):
        return '%s: %s: %s' % (self.checklist.name, self.order, self.text)

class Device(models.Model):
    serial_number = models.CharField(max_length=20)
    user = models.ForeignKey(User)
    checklists = models.ManyToManyField(Checklist)

    def __unicode__(self):
        return '%s: %s' % (self.serial_number, self.user)

class UnregisteredDevice(models.Model):
    serial_number = models.CharField(max_length=20)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-datetime']

    def __unicode__(self):
        return self.serial_number
        
class Data(models.Model):
    data = models.TextField()
    
    def __unicode__(self):
        return self.data
        
class AuditTrail(models.Model):
    data = models.ForeignKey(Data)
    user = models.ForeignKey(User)
    checklist = models.ForeignKey(ChecklistV2)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-datetime']
        
    def __unicode__(self):
        return '%s %s' % (self.user.username, self.checklist.name)
