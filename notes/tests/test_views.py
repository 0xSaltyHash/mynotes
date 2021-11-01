from django.http import response
from django.test import TestCase, Client
from django.urls import reverse
from django.urls.base import resolve
from notes.models import Notes, User


class test_views(TestCase):

    def setUp(self):
        self.client = Client()

    def test_notes_list_logged_in(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('/notes/index.html')
    
    def test_notes_list_not_logged_in(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 302)