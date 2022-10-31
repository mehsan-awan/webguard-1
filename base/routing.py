# from django.conf.urls import url
# from .consumer import GraphConsumer
#
# ws_urlpatterns = [
#     url(r"ws/3/", GraphConsumer.as_asgi()),
#     url(r"ws/17/", GraphConsumer.as_asgi()),
#
# ]

# chat/routing.py
from django.urls import re_path

from .consumer import GraphConsumer

ws_urlpatterns = [
    re_path(r'ws/(?P<user_id>\w+)/$', GraphConsumer.as_asgi()),

]
