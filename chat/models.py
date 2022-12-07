from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    pro_id              = models.AutoField(primary_key=True)
    pro_user            = models.OneToOneField(User, on_delete=models.CASCADE)
    pro_name            = models.TextField(max_length=30)
    pro_picture         = models.ImageField(upload_to='profile')
    pro_updated         = models.DateTimeField(auto_now=True)
    pro_created         = models.DateTimeField(auto_now=True)

class Conservation(models.Model):
    cons_id             = models.AutoField(primary_key=True)
    cons_first          = models.ForeignKey(User, on_delete= models.CASCADE,related_name='first')
    cons_second         = models.ForeignKey(User, on_delete=models.CASCADE,related_name='second')
    
class Chat(models.Model):
    chat_id             = models.AutoField(primary_key=True)
    chat_sender         = models.ForeignKey(User, on_delete= models.CASCADE)
    chat_conservation   = models.ForeignKey("Conservation", on_delete=models.CASCADE)
    chat_text           = models.TextField(max_length=500)
    chat_time           = models.TimeField(auto_now=True)
    chat_date           = models.DateField(auto_now=True)