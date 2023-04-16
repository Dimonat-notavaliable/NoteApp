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
    name = models.CharField(max_length=40, default=None, null=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_absolute_url():
        return '/'

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'


class Topic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic', null=True)
    title = models.CharField('Название', max_length=50)

    def __str__(self):
        return self.title

    @staticmethod
    def get_absolute_url():
        return '/'

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


class Note(models.Model):
    title = models.CharField('Название', max_length=50)
    text = models.TextField('Содержание')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @staticmethod
    def get_absolute_url():
        return '/'

    class Meta:
        abstract = True


class NoteActive(Note):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='note', null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, related_name='topic', blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, related_name='color', blank=True, null=True)

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'

    def place_in_basket(self):
        basket_note = NoteInactive(user=self.user, topic=self.topic, color=self.color, title=self.title,
                                   text=self.text, date_created=self.date_created)
        basket_note.save()
        self.delete()


class NoteInactive(Note):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='note_basket', null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, related_name='topic_basket', blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, related_name='color_basket', blank=True, null=True)
    date_deleted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заметка в корзине'
        verbose_name_plural = 'Заметки в корзине'

    def retrieve(self):
        note = NoteActive(user=self.user, topic=self.topic, color=self.color, title=self.title,
                          text=self.text, date_created=self.date_created)
        note.save()
        self.delete()


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
