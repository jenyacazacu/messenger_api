from .models import Message
from .serializers import MessageSerializer
from rest_framework import generics, mixins, status


class MessageSendView(mixins.CreateModelMixin,
                      generics.GenericAPIView):
    """
    API endpoint that is used to send a message.
    """
    serializer_class = MessageSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MessagesListView(mixins.ListModelMixin,
                       generics.GenericAPIView):
    """
    API Endpoint that lists the recent messages for a given recipient.
    """
    serializer_class = MessageSerializer

    def get_queryset(self):
        """
        Filters the query set depending on the params in the API call
        """
        recipient = self.kwargs['username']
        sender = self.request.query_params.get('sender', None)
        queryset = Message.objects.filter(receiver=recipient)
        if sender is not None:
            queryset = queryset.filter(sender=sender)
        # limit to only the number requested
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

