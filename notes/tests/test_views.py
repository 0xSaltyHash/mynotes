from django.http import response
from django.test import TestCase, Client
from django.urls import reverse
from django.urls.base import resolve
from notes.models import Notes, User
from django.contrib.messages import get_messages

class test_views(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create(username="testuser", password="12345678", email="test@user.mail")
        self.test_note = Notes.objects.create(creator=self.test_user, title="test note", body="test note")
        self.test_note_public = Notes.objects.create(creator=self.test_user, title="public note", body="public note body", is_public=True)
    
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

        self.assertRedirects(response, '/view/3', status_code=302,
         target_status_code=200, fetch_redirect_response=True)

        self.assertEquals(Notes.objects.get(pk=3).title, 'test title')
        self.assertEquals(Notes.objects.get(pk=3).body, 'test body')
    
    def test_create_notes_POST_not_logged_in(self):

        response = self.client.post(reverse('create'), {
            'title': 'test title',
            'body': 'test body'
        })

        self.assertRedirects(response, '/login?next=/create', status_code=302,
         target_status_code=200, fetch_redirect_response=True)

    def test_edit_notes_GET_not_logged_in(self):
        response = self.client.get(reverse('edit', args=[1]))
        self.assertRedirects(response, '/login?next=/edit/1', status_code=302,
        target_status_code=200)
    
    def test_edit_notes_GET_logged_in(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.get(reverse('edit', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('notes/edit.html')
    
    def test_edit_not_found_note_GET_logged_in(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.get(reverse('edit', args=[3]))
        self.assertRedirects(response, '/', status_code=302,
        target_status_code=200)

    def test_edit_not_found_note_POST_logged_in(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.post(reverse('edit', args=[3]), {
            'title': "New test Title",
            "body": 'New Test Body'
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Note doesn't exist")
        self.assertRedirects(response, '/', status_code=302,
        target_status_code=200)

    def test_edit_note_by_non_owner_POST(self):
        self.client.force_login(User.objects.get_or_create(username='testuser2')[0])
        response = self.client.post(reverse('edit', args=[1]), {
            'title': "New test Title",
            "body": 'New Test Body'
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You cannot edit this note")
        self.assertRedirects(response, '/', status_code=302,
        target_status_code=200)

    def test_edit_public_note_by_non_owner_POST(self):
        self.client.force_login(User.objects.get_or_create(username='testuser2')[0])
        response = self.client.post(reverse('edit', args=[2]), {
            'title': "New test Title",
            "body": 'New Test Body'
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You cannot edit this note")
        self.assertRedirects(response, '/', status_code=302,
        target_status_code=200)
    
    def test_edit_note_POST(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.post(reverse('edit', args=[1]), {
            'title': "New Test Title",
            "body": 'New Test Body'
        })

        edited_note = Notes.objects.get(pk=1)        
        messages = list(get_messages(response.wsgi_request))

        self.assertEquals(edited_note.title, "New Test Title")
        self.assertEquals(edited_note.body, "New Test Body")
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Note edited successfuly")
        self.assertRedirects(response, '/view/1', status_code=302,
        target_status_code=200)

    def test_view_private_note_owner_GET(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.get(reverse('view_note', args=[1]))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('notes/note.html')

    def test_view_private_note_not_owner_GET(self):
        self.client.force_login(User.objects.get_or_create(username='testuser2')[0])
        response = self.client.get(reverse('view_note', args=[1]))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You cannot view this note")
        self.assertRedirects(response, '/', status_code=302,
        target_status_code=200)
    
    def test_view_public_note_by_not_owner_GET(self):
        self.client.force_login(User.objects.get_or_create(username='testuser2')[0])
        response = self.client.get(reverse('view_note', args=[2]))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('notes/note.html')
    
    def test_view_note_not_found_GET(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.get(reverse('view_note', args=[3]))
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Note doesn't exist")
        self.assertRedirects(response, '/', status_code=302,
        target_status_code=200)

    def test_view_public_note_not_logged_in_GET(self):
        response = self.client.get(reverse('view_note', args=[2]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('notes/note.html')