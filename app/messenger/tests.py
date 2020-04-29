import random
import string

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from messenger.constants import INT_MAX_MESSAGES_LIMIT
from messenger.models import Message


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def randomText(text_length=8):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(text_length))

    def create_message(self, sender="", recipient=""):
        if sender != "" and recipient != "":
            text = self.randomText()
            Message.objects.create(sender=sender, recipient=recipient, message_content=text)

    def setUp(self):
        # test data
        self.test_user_molly = 'molly'
        self.test_user_ben = 'ben'
        # we will create 50 messages between molly and ben
        for i in range(50):
            self.create_message(sender=self.test_user_molly, recipient=self.test_user_ben)

        self.test_user_alice = 'alice'
        # we will create 50 messages between alice and molly
        for i in range(50):
            self.create_message(sender=self.test_user_alice, recipient=self.test_user_molly)

        # and some between alice and ben
        for i in range(50):
            self.create_message(sender=self.test_user_alice, recipient=self.test_user_ben)

        # test users for message send view tests
        self.test_user_claire = 'claire'
        self.test_user_austin = 'austin'


class MessagesListViewTest(BaseViewTest):
    """
    Testing the MessageListView.
    """

    def test_get_all_messages(self):
        """
        This test ensures that all messages are returned. And the limit requirement is met.
        """
        # request the API endpoint
        response = self.client.get(
            reverse("messages-list")
        )
        self.assertEqual(len(response.data), INT_MAX_MESSAGES_LIMIT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_messages_specific_recipient(self):
        """
        This test ensures that we only return messages for a specific recipient.
        """
        # request the API endpoint
        response = self.client.get(
            reverse("messages-list"), {"recipient": self.test_user_molly})
        # count what is the database
        expected_message_count = Message.objects.filter(recipient=self.test_user_molly).count()
        self.assertEqual(len(response.data), expected_message_count)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_messages_specific_sender(self):
        """
        This test ensures that we only return messages for a specific sender.
        """
        # request the API endpoint
        response = self.client.get(
            reverse("messages-list"), {"sender": self.test_user_alice})
        # count what is the database
        expected_message_count = Message.objects.filter(sender=self.test_user_alice).count()
        self.assertEqual(len(response.data), expected_message_count)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_messages_specific_recipient_and_sender(self):
        """
        This test ensures that we only return messages for a specific recipient and sender.
        """
        # request the API endpoint
        response = self.client.get(
            reverse("messages-list"), {"sender": self.test_user_alice, "recipient": self.test_user_molly})
        # count what is the database
        expected_message_count = Message.objects.filter(
            sender=self.test_user_alice, recipient=self.test_user_molly).count()
        self.assertEqual(len(response.data), expected_message_count)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_unread_messages_specific_recipient(self):
        """
        This test ensures that we only return messages that are new/not read for a specific recipient.
        """
        # lets update all messages that ben received from molly as read
        Message.objects.filter(recipient=self.test_user_ben, sender=self.test_user_molly).update(is_read=True)
        # request the API endpoint
        response = self.client.get(
            reverse("messages-list"), {"recipient": self.test_user_ben, "is_read": False})
        # count what is the database
        expected_message_count = Message.objects.filter(recipient=self.test_user_ben, is_read=False).count()
        self.assertEqual(len(response.data), expected_message_count)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MessagesSendViewTest(BaseViewTest):
    """
    Testing the MessageSendView.
    """

    def test_send_message_success(self):
        """
        This test ensures that a message can be sent successfully.
        """
        request_body = {
            "sender": self.test_user_austin,
            "recipient": self.test_user_claire,
            "message_content": self.randomText()
        }
        response = self.client.post(
            reverse("message-send"),
            request_body
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # check that the database was updated
        ms_count = Message.objects.filter(recipient=self.test_user_claire, sender=self.test_user_austin).count()
        self.assertEqual(ms_count, 1)

    def test_send_message_fail_missing_sender(self):
        """
        This test ensures that a message cannot be sent without a sender.
        """
        request_body = {
            "sender": "",
            "recipient": self.test_user_claire,
            "message_content": self.randomText()
        }
        response = self.client.post(
            reverse("message-send"),
            request_body
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_message_fail_missing_recipient(self):
        """
        This test ensures that a message cannot be sent without a recipient.
        """
        request_body = {
            "sender": self.test_user_claire,
            "recipient": "",
            "message_content": self.randomText()
        }
        response = self.client.post(
            reverse("message-send"),
            request_body
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_message_fail_missing_text(self):
        """
        This test ensures that a message cannot be sent without content.
        """
        request_body = {
            "sender": self.test_user_claire,
            "recipient": self.test_user_claire,
            "message_content": ""
        }
        response = self.client.post(
            reverse("message-send"),
            request_body
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
