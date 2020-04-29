from django.db import models


class Message(models.Model):
    # this max length of 50 should be enough if we use email, username, .. etc.
    # plus it makes it more readable
    sender = models.CharField(max_length=50, blank=False, null=False)
    recipient = models.CharField(max_length=50, blank=False, null=False)
    # the message content is limited to 160 character for readability
    message_content = models.CharField(max_length=160, blank=False)
    sent_datetime = models.DateTimeField(auto_now=True)
    # this field is nice since we can fetch unread messages if we want to
    # given that our API is pretty naive and uses a GET method for messages
    is_read = models.BooleanField(default=False)

    class Meta:
        get_latest_by = "-sent_datetime"
