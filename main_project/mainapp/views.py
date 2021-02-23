from django.shortcuts import render
from django.views.generic import ListView

from main_project.mixins import HTMLTemplateAutoCreateMixin
from .models import Post


class PostListView(ListView, HTMLTemplateAutoCreateMixin):

    model = Post
    template_name = 'post_list.html'
    context_object_name = 'post_list'
    put_context_object_name_in_template = True

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['my_custom_var'] = 1
        context['published'] = self.get_published_posts()
        return context

    def get_published_posts(self):
        return super().get_queryset().filter(published=False)
