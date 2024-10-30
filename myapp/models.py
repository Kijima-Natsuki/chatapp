from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField()
    profile_image = models.ImageField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return self.username
    
class TalkRoom(models.Model):
    users = models.ManyToManyField(CustomUser, related_name='talkrooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TalkRoom {self.id}"
    
class Message(models.Model):
    room = models.ForeignKey(TalkRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"