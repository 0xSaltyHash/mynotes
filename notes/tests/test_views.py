from django.http import response
from django.test import TestCase, Client
from django.urls import reverse
from django.urls.base import resolve
from notes.models import Notes, User


class test_views(TestCase):

    def setUp(self):
        self.client = Client()
        #self.test_user = User.objects.create(username="testuser", password="12345678", email="test@user.mail")

    def test_notes_list_logged_in(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('/notes/index.html')
    
    def test_notes_list_not_logged_in(self):
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/login?next=/', status_code=302,
         target_status_code=200, fetch_redirect_response=True)

    def test_create_notes_GET_logged_in(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.get(reverse('create'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('/notes/create.html')
    
    def test_create_notes_GET_not_logged_in(self):
        response = self.client.get(reverse('create'))
        self.assertRedirects(response, '/login?next=/create', status_code = 302,
        target_status_code=200)

    def test_create_notes_POST_logged_in(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.post(reverse('create'), {
            'title': 'test title',
            'body': 'test body'
        })

        self.assertRedirects(response, '/', status_code=302,
         target_status_code=200, fetch_redirect_response=True)

        self.assertEquals(Notes.objects.get(pk=1).title, 'test title')
        self.assertEquals(Notes.objects.get(pk=1).body, 'test body')
    
    def test_create_notes_POST_logged_in(self):

        response = self.client.post(reverse('create'), {
            'title': 'test title',
            'body': 'test body'
        })

        self.assertRedirects(response, '/login?next=/create', status_code=302,
         target_status_code=200, fetch_redirect_response=True)
