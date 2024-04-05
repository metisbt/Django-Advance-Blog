from django.test import TestCase, Client
from django.urls import reverse

class TestBlogView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_blog_index_url_successful_response(self):
        url = reverse('blog:cbv-index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='index.html')