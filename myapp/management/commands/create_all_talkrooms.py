from django.core.management.base import BaseCommand
from django.db.models import Q
from myapp.models import CustomUser, TalkRoom

class Command(BaseCommand):
    help = 'Create talk rooms between all users'

    def handle(self, *args, **kwargs):
        users = CustomUser.objects.all()
        for user1 in users:
            for user2 in users:
                if user1 != user2:
                    existing_rooms = TalkRoom.objects.filter(users=user1).filter(users=user2)
                    if not existing_rooms.exists():
                        room = TalkRoom.objects.create()
                        room.users.add(user1, user2)
                        room.save()
        self.stdout.write(self.style.SUCCESS('All talk rooms have been created'))