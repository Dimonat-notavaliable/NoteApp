from django.db import models
from register.models import User


class Color(models.Model):
    COLOR_PALETTE = [
        ("#FFFF0090", "yellow",),
        ("#FF000050", "red",),
        ("#00FF0090", "green",),
    ]
    hex = models.CharField('HEX', max_length=10, choices=COLOR_PALETTE)

    def __str__(self):
        return self.hex

    def get_absolute_url(self):
        return '/'

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'


class Topic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic', null=True)
    title = models.CharField('Название', max_length=50)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/'

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='note', null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, related_name='topic', null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, related_name='color', null=True)
    title = models.CharField('Название', max_length=50)
    text = models.TextField('Содержание')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/'

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
