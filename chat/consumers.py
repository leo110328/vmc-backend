# chat/consumers.py
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
from django.db.models import Q

from chat.models import MsgInfo
from common.time_utils import get_int_time
from common.uuid_utils import get_uuid_str
from user.models import UserInfo
from vmc_backend import settings


# 判断当前用户使用登錄


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.room_name = None

    # 在线用户列表
    users = {}

    def is_login(self, token, user_id):
        if token is None:
            if settings.DEBUG:
                print("参数错误,token参数不存在,token = {}".format(token))
            return False
        use_info = cache.get(token)
        if use_info is None:
            if settings.DEBUG:
                print("参数错误,token数据不存在, token = {}".format(token))
            return False
        if len(json.loads(use_info)) <= 0:
            if settings.DEBUG:
                print("参数错误,token数据已过期, token = {}".format(token))
            return False
        if json.loads(use_info)[0]["id"] != user_id:
            if settings.DEBUG:
                print("参数错误,token和聊天室ID不一致,token = {},user_id = ".format(token, user_id))
            return False
        return True

    # 建立链接
    async def connect(self):
        room_name = self.scope['url_route']['kwargs']['room_name']
        token = self.scope['url_route']['kwargs']['token']
        if not self.is_login(token, room_name):
            # 如果用户未登錄,或者token和聊天室ID不一致，关闭连接
            await self.close()
        else:
            # 当前用户的所有连接
            channel_names = [self.channel_name]
            if room_name in self.users:
                channel_names = channel_names + self.users[room_name]
            self.users[room_name] = channel_names

            # 同意连接
            await self.accept()

            chats = await self.query_by_accept_id(room_name)
            for chat in chats:
                text = {"sendId": chat.send_id, "sendName": chat.send_name, "acceptId": chat.accept_id,
                        "msgId": chat.msg_id, "msgType": chat.msg_type,
                        "msgValue": chat.msg_value, "timestamp": chat.timestamp
                        }

                await self.send(text_data=json.dumps({
                    'message': get_to_send_msg(text),
                }, ensure_ascii=False))

                await self.update_or_create(text, chat.id)

    async def disconnect(self, close_code):
        channel_names_item = []
        room_name = self.scope['url_route']['kwargs']['room_name']
        if room_name in self.users:
            channel_names = self.users[room_name]
            if self.channel_name in channel_names:
                channel_names.remove(self.channel_name)
            channel_names_item = channel_names
        if len(channel_names_item) > 0:
            self.users[room_name] = channel_names_item
        else:
            if room_name in self.users.keys():
                self.users.pop(room_name)
        await self.close()

    # 接收用户消息
    async def receive(self, text_data):
        room_name = self.scope['url_route']['kwargs']['room_name']
        token = self.scope['url_route']['kwargs']['token']
        self.is_login(token, room_name)
        chat_msg_to_json = json.loads(json.loads(text_data)['message'])
        chat_msg_to_json["timestamp"] = get_int_time()
        chat_msg_to_json["sendName"] = await self.query_username_by_user_id(chat_msg_to_json["sendId"])
        uuid_item = get_uuid_str()
        # 接收用户发送的消息,将消息入库
        await self.save_msg(chat_msg_to_json, uuid_item)
        # 接收人ID
        accept_id = chat_msg_to_json["acceptId"]
        # 如果接收人已经登錄，则直接发送
        if accept_id in self.users:
            for channel_name in self.users[accept_id]:
                await self.channel_layer.send(
                    channel_name,
                    {
                        'type': 'chat_message',
                        'message': json.dumps(get_to_send_msg(chat_msg_to_json), ensure_ascii=False),
                    }
                )
            # 发送消息到用户之后，将已发送的消息设置為已发送
            await self.update_or_create(chat_msg_to_json, uuid_item)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': [message]
        }, ensure_ascii=False))

    # 保存用户发送的消息到数据库
    @database_sync_to_async
    def save_msg(self, text_data_json, uuid_item):
        MsgInfo.objects.create(id=uuid_item, send_id=text_data_json['sendId'], send_name=text_data_json['sendName'],
                               accept_id=text_data_json['acceptId'],
                               msg_type=text_data_json['msgType'],
                               msg_id=text_data_json['msgId'],
                               msg_value=text_data_json['msgValue'], timestamp=text_data_json["timestamp"],
                               send_success="0")

    @database_sync_to_async
    def update_or_create(self, text_data_json, uuid_item):
        MsgInfo.objects.update_or_create(defaults={'send_success': "1"}, id=uuid_item,
                                         send_id=text_data_json['sendId'], send_name=text_data_json['sendName'],
                                         accept_id=text_data_json['acceptId'],
                                         msg_type=text_data_json['msgType'],
                                         msg_id=text_data_json['msgId'],
                                         msg_value=text_data_json['msgValue'], timestamp=text_data_json["timestamp"])

    @database_sync_to_async
    def query_by_accept_id(self, accept_id):
        chats = MsgInfo.objects.filter(accept_id=accept_id, send_success="0")
        return list(chats)

    @database_sync_to_async
    def query_username_by_user_id(self, user_id):
        user_name_key = "user_name_" + user_id
        user_name = cache.get(user_name_key)
        if not user_name is None:
            return user_name
        user_info = UserInfo.objects.filter(Q(id=user_id))
        user_name_value = "none"
        if len(user_info) > 0:
            user_name_value = user_info[0].username
        cache.set(user_name_key, user_name_value)
        return user_name_value


def get_to_send_msg(text_json):
    item = {"sendId": text_json["sendId"], "sendName": text_json["sendName"], "acceptId": text_json["acceptId"],
            "msgId": text_json["msgId"], "msgValue": text_json["msgValue"], "sendTime": text_json["timestamp"]
            }
    return item
