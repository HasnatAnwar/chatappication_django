from channels.consumer import SyncConsumer , AsyncConsumer ,async_to_sync 
from channels.exceptions import StopConsumer
from .models import *
import json
from .serial import *
from rest_framework.permissions import IsAdminUser , IsAuthenticated ,  BasePermission
from rest_framework.decorators import authentication_classes , permission_classes
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs      


class message(SyncConsumer):
    def websocket_connect(self,event):
        print('Treid here')
        try:
            token_key = parse_qs(self.scope['query_string'].decode("utf8"))['token'][0]
            token = Token.objects.get(key=token_key)
            self.user = token.user
            # print(self.user)
        except Token.DoesNotExist:            
            self.user = AnonymousUser()
        self.group_name = self.scope['url_route']['kwargs']['pk']
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
            )
        self.send({
            'type':'websocket.accept'
        })
    def websocket_receive(self,event):
        if self.user.is_authenticated:
            dataa = json.loads(event['text'])
            try:
                comment = Chat.objects.create(
                    chat_sender = User.objects.get(username=self.user),
                    chat_text = dataa['chat_text'],
                    chat_conservation = Conservation.objects.get(cons_id=int(self.group_name))
                )
                serial = ChatSerial(comment).data
                async_to_sync(self.channel_layer.group_send)(
                    self.group_name,
                        {
                        'type':'chat.message',
                        'message':serial
                    })
            except:
                self.send({
                    'type':'websocket.send',
                    'text':json.dumps({"message":"Invalid Input"})
                })    
        else:
            self.send({
                'type':'websocket.send',
                'text':json.dumps({"message":"Login Required"})
            })
    def chat_message(self,event):
        self.send({
            'type':'websocket.send',
            'text':str(event['message'])
        })

    def websocket_disconnect(self,event):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
            )
        raise StopConsumer()