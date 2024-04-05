from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime

from blog.models import Post, Category
from accounts.models import User, Profile

class TestBlogView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='ali@ali.com', password='a@/123456')
        self.profile = Profile.objects.create(
            user = self.user,
            first_name = 'ali test',
            last_name = 'ali test',
            description = 'description test',
        )
        self.post = Post.objects.create(
            title = 'test for test model',
            content = 'description',
            status = True,
            category = None,
            author = self.profile,
            published_date = datetime.now()
        )

    def test_blog_index_url_successful_response(self):
        url = reverse('blog:cbv-index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='index.html')

    def test_blog_post_detail_logged_in_response(self):
        # for login required pages
        self.client.force_login(self.user)
        url = reverse('blog:post-detail',kwargs={'pk':self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_blog_post_detail_anonymous_response(self):
        url = reverse('blog:post-detail',kwargs={'pk':self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)