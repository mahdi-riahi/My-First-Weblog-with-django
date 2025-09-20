from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse

from .models import Post, Comment


class BlogTest(TestCase):
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
        cls.comment = Comment.objects.create(
            author='Mehrdad',
            text='Awesome comment',
            related_post=cls.post1,
        )

    # Post model and objects
    def test_post_model_str(self):
        self.assertEqual(self.post1.title, str(self.post1))

    def test_post_model_get_absolute_url(self):
        self.assertEqual(self.post1.get_absolute_url(), reverse('post_detail', args=[self.post1.id]))

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

    def test_post_list_read_more_button(self):
        response = self.client.get(reverse('post_list'))
        self.assertContains(response, 'Read More  |  comment & edit post')

    # post-detail
    def test_post_detail_url(self):
        response1 = self.client.get(f'/blog/{self.post2.id}/')
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.get(reverse('post_detail', args=[self.post2.id, ]))
        self.assertEqual(response2.status_code, 200)

    def test_post_detail_not_found_404(self):
        response = self.client.get(reverse('post_detail', args=[self.post2.id + 1, ]))
        self.assertEqual(response.status_code, 404)

    def test_post_detail(self):
        response = self.client.get(reverse('post_detail', args=[self.post2.id, ]))
        self.assertContains(response, self.post2.title)
        self.assertContains(response, self.post2.content)
        self.assertContains(response, self.post2.author.username)

    def test_post_detail_buttons(self):
        response = self.client.get(f'/blog/{self.post1.id}/')
        self.assertContains(response, 'Edit Post')
        self.assertContains(response, 'Delete Post')

    # post-create
    def test_post_create_url(self):
        response1 = self.client.get(reverse('post_create'))
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.get('/blog/create_post/')
        self.assertEqual(response2.status_code, 200)

    def test_post_create(self):
        response = self.client.post(reverse('post_create'), {
            'title': 'my title',
            'content': 'my content',
            'status': 'p',
            'author': self.user.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'my title')
        self.assertEqual(Post.objects.last().content, 'my content')
        self.assertEqual(Post.objects.last().status, 'p')
        self.assertEqual(Post.objects.last().author, self.user)

    # post-update
    def test_post_update_url(self):
        response1 = self.client.get(f'/blog/{self.post2.id}/update/')
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.get(reverse('post_update', args=[self.post2.id, ]))
        self.assertEqual(response2.status_code, 200)

    def test_post_update_not_found_404(self):
        response = self.client.get(reverse('post_update', args=[self.post2.id + 1, ]))
        self.assertEqual(response.status_code, 404)

    def test_post_update_get_old_details(self):
        response = self.client.get(reverse('post_update', args=[self.post2.id, ]))
        self.assertContains(response, self.post2.title)
        self.assertContains(response, self.post2.content)
        self.assertContains(response, self.post2.author.username)

    def test_post_update_post_new_details(self):
        response = self.client.post(reverse('post_update', args=[self.post2.id, ]), {
            'title': 'new title',
            'content': 'new content',
            'status': 'p',
            'author': self.user.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.get(pk=self.post2.id).title, 'new title')
        self.assertEqual(Post.objects.get(pk=self.post2.id).content, 'new content')
        self.assertEqual(Post.objects.get(pk=self.post2.id).status, 'p')
        self.assertEqual(Post.objects.get(pk=self.post2.id).author, self.user)

    # post-delete
    def test_post_delete_url(self):
        response1 = self.client.get(f'/blog/{self.post2.id}/delete/')
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.get(reverse('post_delete', args=[self.post2.id, ]))
        self.assertEqual(response2.status_code, 200)

    def test_post_delete_not_found_404(self):
        response = self.client.get(reverse('post_delete', args=[self.post2.id + 1, ]))
        self.assertEqual(response.status_code, 404)

    def test_post_delete_detail(self):
        response = self.client.get(reverse('post_delete', args=[self.post2.id, ]))
        self.assertContains(response, self.post2.title)

    def test_post_delete(self):
        response = self.client.post(f'/blog/{self.post2.id}/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(Post.objects.last().title, 'title2')
        self.assertNotEqual(Post.objects.last().content, 'content2')

    # comment model and objects
    def test_comment_model_str(self):
        self.assertEqual(self.comment.text, str(self.comment))

    def test_comment_object_detail(self):
        self.assertEqual(self.comment.author, 'Mehrdad')
        self.assertEqual(self.comment.text, 'Awesome comment')
        self.assertEqual(self.comment.related_post, self.post1)

    def test_comment_existence_for_post1(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id, ]))
        self.assertContains(response, self.comment.author)
        self.assertContains(response, self.comment.text)

    def test_comment_existence_for_post2(self):
        response = self.client.get(reverse('post_detail', args=[self.post2.id, ]))
        self.assertNotContains(response, self.comment.text)

    def test_comment_post_new_comment(self):
        response = self.client.post(reverse('post_detail', args=[self.post2.id, ]), {
            'author': 'david',
            'text': 'this is awesome.',
            'email_address': 'davidcopperfield111@yahoo.com',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.last().author, 'david')
        self.assertEqual(Comment.objects.last().text, 'this is awesome.')
        self.assertEqual(Comment.objects.last().email_address, 'davidcopperfield111@yahoo.com')
        self.assertEqual(Comment.objects.last().related_post, self.post2)
