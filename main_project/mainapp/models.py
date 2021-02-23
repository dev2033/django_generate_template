from django.db import models


class Post(models.Model):
    """Пост"""
    title = models.CharField('Название поста', max_length=100)
    content = models.TextField('Контент поста')
    published = models.BooleanField('Опубликовано', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
