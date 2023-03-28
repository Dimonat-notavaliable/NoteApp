from django.db import models
from register.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task', null=True)
    title = models.CharField('Название', max_length=50)
    task = models.TextField('Описание')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/'

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
