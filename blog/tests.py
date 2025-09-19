from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse

from .models import Post, Comment


class PostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Nayebzad')
        cls.post1 = Post.objects.create(
            title='title1',
            content='content1',
            status='p',
            author=cls.user,
        )
        cls.post2 = Post.objects.create(
            title='title2',
            content='content2',
            status='d',
            author=cls.user,
        )

    # objects and models
    def test_post_model_str(self):
        self.assertEqual(self.post1.title, str(self.post1))

    def test_post_object_detail(self):
        self.assertEqual(self.post1.title, 'title1')
        self.assertEqual(self.post1.content, 'content1')
        self.assertEqual(self.post1.status, 'p')
        self.assertEqual(self.post1.author, self.user)

    # post-list
    def test_post_list_url(self):
        response1 = self.client.get('/blog/')
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.get(reverse('post_list'))
        self.assertEqual(response2.status_code, 200)

    def test_post_list_show_status_p(self):
        response = self.client.get(reverse('post_list'))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.content)

    def test_post_list_show_status_d(self):
        response = self.client.get(reverse('post_list'))
        self.assertNotContains(response, self.post2.title)
        self.assertNotContains(response, self.post2.content)

    # post-detail

