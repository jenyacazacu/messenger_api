from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'message_content', 'sent_datetime', 'is_read']
        read_only_fields = ['sent_datetime', 'is_read']
