from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_message, name='send_message'),
    path('send/<str:recipient_username>/', views.send_message, name='send_message_to'),
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent, name='sent'),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
     path('thread/<str:recipient_username>/', views.message_thread, name='message_thread'),
]