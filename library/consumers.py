import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from library.models import Book


class BookConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name='book_notifications'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are connected to book notifications!'
        }))

    async def disconnect(self):
        
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data ):

        data = json.loads(text_data)
        mesage_type= data.get('type','unknown')

        if mesage_type == 'ping':

            await self.send(text_data=json.dumps({
                'type':'pong',
                'message':'server is alive'
            }))

    
        elif mesage_type=='get_book_count':
             count = await self.get_book_count()
             await self.send(text_data=json.dumps({
                 'type':'book_count',
                 'count':count
             }))

    async def book_created(self, event):
         
         await self.send(text_data=json.dumps({
             'type':'book_created',
             'event':event['book']
         }))
    
    async def book_deleted(self, event):

        await self.send(text_data=json.dumps({
            'type':'book_deleted',
            'event':event['book_id'],
            'message':event['message']
        }))

    @database_sync_to_async
    def get_book_count(self):
        return Book.objects.count()

    

    