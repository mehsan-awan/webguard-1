from channels.generic.websocket import AsyncWebsocketConsumer
import json


class GraphConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user_id = self.scope["path"]
        user_id = user_id.split("/")[-2]

        self.groupname = "dashboard{}".format(user_id)
        print(self.groupname)

        # self.groupname = 'dashboard'

        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name,
        )
        await self.accept()

        print("Socket Connected")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )
        print("Socket Disconnected")

    async def receive(self, text_data):
        datapoint = json.loads(text_data)
        val = datapoint['value']
        val2 = datapoint['value2']
        # val3 = datapoint['value3']
        # val4 = datapoint['value4']

        await self.channel_layer.group_send(
            self.groupname,
            {
                'type': 'deprocessing',
                'value': val,
                'value2': val2,
                # 'value3': val3,
                # 'value4': val4
            }
        )

    async def deprocessing(self, event):
        valOther = event['value']
        valOther2 = event['value2']
        # valOther3 = event['value3']
        # valOther4 = event['value4']
        # await self.send(
        #     text_data=json.dumps({'value': valOther, 'value2': valOther2, 'value3': valOther3, 'value4': valOther4}))

        await self.send(
            text_data=json.dumps({'value': valOther, 'value2': valOther2}))

