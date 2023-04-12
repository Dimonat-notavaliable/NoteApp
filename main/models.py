from django.db import models
from django.core.cache import cache
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


class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)
        self.set_cache()

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)


class SiteLinks(SingletonModel):
    class Meta:
        verbose_name = 'Поддержка сайта'
        verbose_name_plural = 'Поддержка сайта'

    support = models.EmailField(default='NoteAppTPU@yandex.ru')
    vk = models.CharField(max_length=50, blank=True)
    telegram = models.CharField(max_length=50, blank=True)
    instagram = models.CharField(max_length=50, blank=True)
