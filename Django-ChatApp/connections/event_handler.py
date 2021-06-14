from connections.utils import  HTTPClientException
import tornado.web
import tornado.httpclient
import tornado.gen, json
from .config import  UPDATE_MESSAGE_DETAILS, UPDATE_GROUP_DETAILS

class EventHandler(object):

    def __init__(self, payload, client):
        self.payload =  payload
        self.client = client

    def update_message_details_api(self):

        api_endpoint = UPDATE_MESSAGE_DETAILS

        request_body = self.payload

        try:
            self.async_http_api_fetch(
                api_endpoint=api_endpoint,
                method="POST",
                request_body=request_body,
                callback=self.handle_response
            )
        except HTTPClientException as e:
            print(e)

    def update_group_details_api(self):

        api_endpoint = UPDATE_GROUP_DETAILS

        request_body = self.payload

        try:
            self.async_http_api_fetch(
                api_endpoint=api_endpoint,
                method="POST",
                request_body=request_body,
                callback=self.handle_response
            )
        except HTTPClientException as e:
            print(e)


    def handle_response(self, response):
        """
        Method used for handling the response of API handlers
        :param response: response from API
        """
        data = json.loads(response.body.decode())
        status = data.get("status")
        if status and 'users' in data:
            for user in data.get("users"):
                if str(user) in self.client:
                    self.client[str(user)].write_message(data.get("message"))


    def async_http_api_fetch(self, api_endpoint, method='GET',
                             request_body=None, callback=None):


        # if not callback:
        #     raise HTTPClientException(
        #         "callback is not provided."
        #     )

        http_client = tornado.httpclient.AsyncHTTPClient(defaults=dict(request_timeout=180))

        return http_client.fetch(
            tornado.httpclient.HTTPRequest(
                api_endpoint, method,

                body=json.dumps(
                    request_body
                )
            ),
            callback=callback
        )


