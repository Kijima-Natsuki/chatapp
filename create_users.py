import os
import random

import django
from dateutil import tz
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intern.settings")
django.setup()

from myapp.models import Message, CustomUser, TalkRoom

fakegen = Faker(["ja_JP"])

def create_users(n):
    users = [
        CustomUser(username=fakegen.user_name(), email=fakegen.ascii_safe_email())
        for _ in range(n)
    ]

    CustomUser.objects.bulk_create(users, ignore_conflicts=True)

    my_id = CustomUser.objects.get(username="admin").id

    created_users = CustomUser.objects.filter(username__in=[user.username for user in users])
    user_ids = list(created_users.values_list("id", flat=True))

    rooms = []
    for user_id in user_ids:
        room = TalkRoom.objects.create()
        room.users.add(user_id, my_id)
        room.save()
        rooms.append(room)

    talks = []
    for _ in range(len(user_ids)):
        room = random.choice(rooms)
        sender = random.choice([my_id, room.users.exclude(id=my_id).first().id])

        message = Message(
            room=room,
            sender_id=sender,
            content=fakegen.text(),
        )
        talks.append(message)
    Message.objects.bulk_create(talks, ignore_conflicts=True)

    talks = Message.objects.order_by("-time")[: 2 * len(user_ids)]
    for talk in talks:
        talk.timestamp = fakegen.date_time_this_year(tzinfo=tz.gettz("Asia/Tokyo"))
    Message.objects.bulk_update(talks, fields=["time"])

if __name__ == "__main__":
    print("creating users ...", end="")
    create_users(970)
    print("done")
