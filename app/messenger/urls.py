from django.urls import path
from messenger import views

urlpatterns = [
     path('messages/send/', views.MessageSendView.as_view(), name='message-send'),
     path('messages/', views.MessagesListView.as_view(), name='messages-list'),
]
