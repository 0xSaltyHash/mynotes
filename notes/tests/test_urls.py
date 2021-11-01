from django.test import SimpleTestCase
from django.urls import reverse, resolve
from notes.views import index, create, edit, note

class TestUrls(SimpleTestCase):
    
    def test_index_url_is_resolved(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index) 
    
    def test_create_url_is_resolved(self):
        url = reverse('create')
        self.assertEquals(resolve(url).func, create)
    
    def test_edit_url_is_resolved(self):
        url = reverse('edit', args=[1])
        self.assertEquals(resolve(url).func, edit)

    def test_view_url_is_resolver(self):
        url = reverse('view_note', args=[1])
        self.assertEquals(resolve(url).func, note)