from django.contrib import admin

# Register your models here.

from .models import CustomUser, TalkRoom, Message

admin.site.register(CustomUser)
admin.site.register(TalkRoom)
admin.site.register(Message)