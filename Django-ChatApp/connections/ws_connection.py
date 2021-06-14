import json
from connections.event_handler import EventHandler
import tornado.gen
import tornado.websocket


clients = {}

class EchoWebSocket(tornado.websocket.WebSocketHandler):

    def __init__(self, application, request, **kwargs):

        super(EchoWebSocket, self).__init__(application, request, **kwargs)
        self.client_id = str(self.get_argument("current_user"))

    def check_origin(self, origin):
        return True

    def open(self):
        print("WebSocket opened")
        print('connection for client {0} opened...'.format(self.client_id))
        clients[self.client_id] = self

    def on_message(self, message):
        payload = json.loads(message)
        meta_info = payload.get("meta")
        if 'group_id' in meta_info:
            self.send_group_messages(meta_info, payload)
        else:
            self.send_friend_messages(meta_info, payload)



    def on_close(self):
        clients.pop(self.client_id, None)
        print("WebSocket closed")

    def send_friend_messages(self, meta_info, payload):

        client_id = meta_info.get("receiver_id")
        message = payload.get("message")
        request_handler = EventHandler(payload)
        request_handler.update_message_details_api()
        if client_id in clients:
            clients[client_id].write_message(message)

    def send_group_messages(self, meta_info, payload):

        request_handler = EventHandler(payload, clients)
        request_handler.update_group_details_api()




