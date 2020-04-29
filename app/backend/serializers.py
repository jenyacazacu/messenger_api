from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'message_content', 'created', 'is_read']
        read_only_fields = ['created', 'is_read']
