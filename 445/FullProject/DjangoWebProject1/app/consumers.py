import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


from channels.layers import get_channel_layer



class ChatConsumer(WebsocketConsumer):
    #def __init__(self):
    #    super().__init__()
    #    self.channel_layer = get_channel_layer()
    #    self.channel_name = self.channel_layer.new_channel()
        #self.room_group_name = 

    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
   

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message
            }
        )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message': message }))
            