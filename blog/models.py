from django.db import models
from django.shortcuts import reverse


class Post(models.Model):
    STATUSES = (
        ('p', 'published'),
        ('d', 'draft'),
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUSES)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id])


class Comment(models.Model):
    author = models.CharField(max_length=50)
    text = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    related_post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)
    email_address = models.EmailField(default='example@example.com')

    def __str__(self):
        return self.text
