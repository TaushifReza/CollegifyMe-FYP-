import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from chat.models import Thread, ChatMessage
from user.models import User
from student.models import StudentProfile
from college.models import CollegeProfile


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connect", event)
        user = self.scope["user"]
        chat_room = f"user_chatroom_{user.id}"
        self.chat_room = chat_room
        await self.channel_layer.group_add(chat_room, self.channel_name)
        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, event):
        print("receive", event)
        received_data = json.loads(event["text"])
        msg = received_data.get("message")
        sent_by_id = received_data.get("sent_by")
        send_to_id = received_data.get("send_to")
        thread_id = received_data.get("thread_id")
        if not msg:
            print("Error:: empty message")
            return False

        sent_by_user = await self.get_user_object(sent_by_id)
        send_to_user = await self.get_user_object(send_to_id)
        thread_obj = await self.get_thread(thread_id)
        if not sent_by_user:
            print("Error:: sent by user is incorrect")
        if not send_to_user:
            print("Error:: send to user is incorrect")
        if not thread_obj:
            print("Error:: Thread id is incorrect")

        # Save Chat Message to db
        await self.create_chat_message(thread_obj, sent_by_user, msg)

        other_user_chat_room = f"user_chatroom_{send_to_id}"
        self_user = self.scope["user"]

        # sent by info
        sent_by_info = await self.get_sent_by_info(sent_by_id)
        # sent to info
        sent_to_info = await self.get_sent_to_info(send_to_id)

        response = {
            "message": msg,
            "sent_by": self_user.id,
            "thread_id": thread_id,
            "sent_by_info": sent_by_info,
            "sent_to_info": sent_to_info,
        }

        await self.channel_layer.group_send(
            other_user_chat_room,
            {
                "type": "chat_message",
                "text": json.dumps(response),
            },
        )

        await self.channel_layer.group_send(
            self.chat_room,
            {
                "type": "chat_message",
                "text": json.dumps(response),
            },
        )

    async def websocket_disconnect(self, event):
        print("disconnect", event)

    async def chat_message(self, event):
        print("chat_message", event)
        await self.send({"type": "websocket.send", "text": event["text"]})

    @database_sync_to_async
    def get_user_object(self, user_id):
        qs = User.objects.filter(id=user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def get_thread(self, thread_id):
        qs = Thread.objects.filter(id=thread_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def create_chat_message(self, thread, user, msg):
        ChatMessage.objects.create(thread=thread, user=user, message=msg)

    @database_sync_to_async
    def get_sent_by_info(self, sent_by_id):
        user = User.objects.get(id=sent_by_id)
        user_info = {"id": user.id, "email": user.email, "role": user.role}
        if user.role == 1:
            user_profile = StudentProfile.objects.get(user=user)
            user_profile_info = {
                "id": user_profile.id,
                "user_id": user_profile.user.id,
                "first_name": user_profile.first_name,
                "profile_image": user_profile.profile_image.url,
            }
        else:
            user_profile = CollegeProfile.objects.get(user=user)
            user_profile_info = {
                "id": user_profile.id,
                "user_id": user_profile.user.id,
                "first_name": user_profile.college_name,
                "profile_image": user_profile.college_logo.url,
            }
        return {"user": user_info, "user_prfile": user_profile_info}

    @database_sync_to_async
    def get_sent_to_info(self, sent_to_id):
        user = User.objects.get(id=sent_to_id)
        user_info = {
            "id": user.id,
            "email": user.email,
            "role": user.role,
        }
        if user.role == 1:
            user_profile = StudentProfile.objects.get(user=user)
            user_profile_info = {
                "id": user_profile.id,
                "user_id": user_profile.user.id,
                "first_name": user_profile.first_name,
                "profile_image": user_profile.profile_image.url,
            }
        else:
            user_profile = CollegeProfile.objects.get(user=user)
            user_profile_info = {
                "id": user_profile.id,
                "user_id": user_profile.user.id,
                "first_name": user_profile.college_name,
                "profile_image": user_profile.college_logo.url,
            }
        return {"user": user_info, "user_prfile": user_profile_info}
