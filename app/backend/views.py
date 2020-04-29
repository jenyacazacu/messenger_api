from datetime import datetime, timedelta
from rest_framework import generics, mixins

from backend.constants import INT_MAX_MESSAGES_LIMIT, INT_MAX_DAYS_OFFSET
from .models import Message
from .serializers import MessageSerializer


class MessageSendView(mixins.CreateModelMixin,
                      generics.GenericAPIView):
    """
    API endpoint that is used to send a message.

    Recipient and Sender can be any character representation, email, username, phone number etc.

    Required fields: sender, recipient, message_content.

    Possible response statuses: 201 Created, 400 Bad Request, 500 Server Error.
    """
    serializer_class = MessageSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MessagesListView(mixins.ListModelMixin,
                       generics.GenericAPIView):
    """
    API Endpoint that lists the recent messages for a given recipient.

    It will return all the messages in the last 30 days or a limit of last 100 messages.

    (Optional) query_param 'sender' can be passed in to get all the messages to a recipient from this specific sender.
    If not provided all the messages to this recipient will be returned ordered by send datetime.

    Possible response statuses: 200 OK, 500 Server Error
    """
    serializer_class = MessageSerializer

    def get_queryset(self):
        """
        Filters the query set depending on the parameters in the API call.
        """
        recipient = self.kwargs['username']
        sender = self.request.query_params.get('sender', None)

        # Optional Parameters
        # This are here due to not being 100 clear on the requirements
        # limit = self.request.query_params.get('limit', None)
        # days_offset = self.request.query_params.get('days_offset', None)

        # base query set, this is lazy loaded so no database reads are done at this time
        queryset = Message.objects.filter(receiver=recipient)

        # filter based on sender
        if sender is not None:
            queryset = queryset.filter(sender=sender)

        # create the date in the past, 30 days back
        datetime_in_the_past = datetime.now() - timedelta(days=INT_MAX_DAYS_OFFSET)
        # filter to return everything in the last 30 days, with a limit of 100 messages total
        # order by sent_datetime descending,
        # and sender name secondary so the same timestamp with be alphabetically ordered
        return queryset.filter(sent_datetime__gte=datetime_in_the_past).order_by('-sent_datetime', "sender")[:100]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
