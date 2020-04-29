from datetime import datetime, timedelta
from rest_framework import generics, mixins

from messenger.constants import INT_MAX_MESSAGES_LIMIT, INT_MAX_DAYS_OFFSET
from .models import Message
from .serializers import MessageSerializer


class MessageSendView(mixins.CreateModelMixin,
                      generics.GenericAPIView):
    """
    ### API endpoint to send a short text message.
    ---
    **Request Body Model**

    ```
    {
      "sender": "string",
      "recipient": "string"
      "message_content": "string"
    }
    ```

    **Required:** sender, recipient, message_content

    **Response Model**

    ```
    {
      "id": "int",
      "sender": "string",
      "recipient": "string",
      "message_content": "string",
      "is_read": "bool",
      "sent_datetime": "datetime"
    }
    ```
    ---
    Response Status: 201 Created, 400 Bad Request, 500 Server Error.
    """
    serializer_class = MessageSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MessagesListView(mixins.ListModelMixin,
                       generics.GenericAPIView):
    """
    ### API Endpoint that lists the recent messages.
    ---

    Returns all the messages sent in the last 30 days
    or a limit of last 100 messages, ordered by timestamp descending.

    **Query Params:**

    **'sender'** string (optional)

    **'recipient'** string(optional)

    **'is_read'** boolean (optional)

    ---
    **Response Model**

    ```
    [{
      "id": "int",
      "sender": "string",
      "recipient": "string",
      "message_content": "string",
      "is_read": "bool",
      "sent_datetime": "datetime"
    },...]
    ```

    ---
    **Response Status**: 200 OK, 500 Server Error
    """
    serializer_class = MessageSerializer

    def get_queryset(self):
        """
        Filters the query set depending on the query parameters in the API call.
        """
        queryset = Message.objects.all()

        # start filtering
        recipient = self.request.query_params.get('recipient')
        if recipient is not None:
            queryset = queryset.filter(recipient=recipient)

        sender = self.request.query_params.get('sender', None)
        if sender is not None:
            queryset = queryset.filter(sender=sender)

        is_read = self.request.query_params.get('is_read', None)
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read)

        # create a datetime object based on the constant 30 days back
        # this can be later configured
        datetime_in_the_past = datetime.now() - timedelta(days=INT_MAX_DAYS_OFFSET)

        # filter to return everything in the last 30 days, with a limit of 100 messages total
        # order by sent_datetime descending,
        # and sender name secondary so the same timestamp with be alphabetically ordered
        return queryset.filter(sent_datetime__gte=datetime_in_the_past).order_by('-sent_datetime', "sender")[:100]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
