from django.test import TestCase
from datetime import datetime

from blog.models import Post
from accounts.models import User, Profile

class TestPostModel(TestCase):

    def test_create_post_with_valid_data(self):
        user = User.objects.create_user(email='ali@ali.com', password='a@/123456')
        profile = Profile.objects.create(
            user = user,
            first_name = 'ali test',
            last_name = 'ali test',
            description = 'description test',
        )
        post = Post.objects.create(
            title = 'test for test model',
            content = 'description',
            status = True,
            category = None,
            author = profile,
            published_date = datetime.now()
        )
        self.assertEqual(post.title, 'test for test model')