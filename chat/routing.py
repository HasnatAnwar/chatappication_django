from django.urls import path
from . import consumers

websocket_urlpatterns =[

    path('message/<str:pk>/',consumers.message.as_asgi()),
    
]