from django.test import TestCase
from datetime import datetime

from blog.models import Post
from accounts.models import User, Profile

class TestPostModel(TestCase):

    # for using user and profile object without create each time
    def setUp(self):
        self.user = User.objects.create_user(email='ali@ali.com', password='a@/123456')
        self.profile = Profile.objects.create(
            user = self.user,
            first_name = 'ali test',
            last_name = 'ali test',
            description = 'description test',
        )

    def test_create_post_with_valid_data(self):
        
        post = Post.objects.create(
            title = 'test for test model',
            content = 'description',
            status = True,
            category = None,
            author = self.profile,
            published_date = datetime.now()
        )
        # self.assertEqual(post.title, 'test for test model')
        self.assertTrue(Post.objects.filter(pk=post.id).exists())