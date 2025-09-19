from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy

from . import models
from . import forms


class PostListView(generic.ListView):
    model = models.Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return models.Post.objects.filter(status='p').order_by('-datetime_updated')


def post_detail_view(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    comments = models.Comment.objects.filter(related_post=post)
    comment_form = forms.CommentForm()
    if request.method == "POST":
        comment_form = forms.CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.related_post = post
            comment.save()
            comment_form = forms.CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})


class PostCreateView(generic.CreateView):
    form_class = forms.PostForm
    template_name = 'blog/post_create.html'


class PostUpdateView(generic.UpdateView):
    model = models.Post
    template_name = 'blog/post_create.html'
    form_class = forms.PostForm


class PostDeleteView(generic.DeleteView):
    model = models.Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('post_list')
