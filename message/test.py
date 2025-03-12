from django.test import TestCase, Client
from django.urls import reverse
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.message = Message.objects.create(sender=self.user1, recipient=self.user2, body='Test message')

    def test_message_model(self):
        self.assertEqual(str(self.message), f"From user1 to user2: Test message")
        self.assertFalse(self.message.is_read)

    def test_inbox_view(self):
        self.client.login(username='user2', password='password2')
        response = self.client.get(reverse('inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test message')

    def test_message_detail_view(self):
        self.client.login(username='user2', password='password2')
        response = self.client.get(reverse('message_detail', args=[self.message.id]))
        self.assertEqual(response.status_code, 200)
        self.message.refresh_from_db()
        self.assertTrue(self.message.is_read)

    def test_send_message_view(self):
        self.client.login(username='user1', password='password1')
        response = self.client.post(reverse('send_message'), {'recipient': self.user2.id, 'body': 'New message'})
        self.assertEqual(response.status_code, 302) #Redirects
        self.assertEqual(Message.objects.filter(sender=self.user1, recipient=self.user2).count(), 2)

    def test_message_thread_view(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('message_thread', args=[self.user2.username]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test message')