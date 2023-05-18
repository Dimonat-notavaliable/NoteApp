from abc import ABC, abstractmethod
from datetime import datetime

from django.core.cache import cache
from django.db import models
from django.http import HttpResponse

from translate import Translator
from main.utils import html_2_pdf
from register.models import User


class ResponseFactory:
    def factory_method(self, note):
        return HttpResponse()

    def check(self, note):
        # Вызываем фабричный метод, чтобы получить объект.
        obj = self.factory_method(note)
        # Проверяем расширение файла.
        extension = obj._content_type_for_repr.split('/')[1][:-1]
        result = f'После выполнения операции создания получен файл типа: {extension}'
        return result


class TXTResponse(ResponseFactory):

    def factory_method(self, note):
        title = str(note.title)
        file_data = title + "\n\n" + note.text
        return HttpResponse(file_data, content_type='application/text charset=utf-8')


class PDFResponse(ResponseFactory):

    def factory_method(self, note):
        pdf = html_2_pdf('main/pdf_note.html', {'note': note})
        return HttpResponse(pdf, content_type='application/pdf')


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

class Note(models.Model):
    title = models.CharField('Название', max_length=50)
    text = models.TextField('Содержание')
    date_created = models.DateTimeField()

    def __str__(self):
        return self.title

    @staticmethod
    def get_absolute_url():
        return '/'

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = datetime.now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class NoteActive(Note):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='note', null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, related_name='note', blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, related_name='note', blank=True, null=True)

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'

    def place_in_basket(self):
        mediator = NoteMediator()
        mediator.convert(self)

    def download(self, extension):
        factories = {'pdf': PDFResponse(), 'txt': TXTResponse()}
        factory = factories[extension]
        return factory.factory_method(self)


class NoteInactive(Note):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='note_basket', null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, related_name='topic_basket', blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, related_name='note_basket', blank=True, null=True)
    date_deleted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заметка в корзине'
        verbose_name_plural = 'Заметки в корзине'

    def retrieve(self):
        mediator = NoteMediator()
        mediator.convert(self)


class NoteMediator:
    def __init__(self):
        self._convertible = None
        self._converted = None

    def convert(self, note):
        self._convertible = note
        note_data = {'user': note.user, 'topic': note.topic,
                     'color': note.color, 'title': note.title,
                     'text': note.text, 'date_created': note.date_created}
        if isinstance(note, NoteActive):
            self._converted = NoteInactive(**note_data)
        elif isinstance(note, NoteInactive):
            self._converted = NoteActive(**note_data)
        else:
            raise ValueError()
        self._converted.save()
        self._convertible.delete()
        return self._converted

    class Meta:
        abstract = True


# Proxy pattern
class NoteProtector(Note):
    def __init__(self, note: Note):
        self.note = note

    def place_in_basket(self, request_user: User):
        if (self.note.user == request_user) or request_user.is_superuser:
            self.note.place_in_basket()
            return f'Заметка "{self.note.title}" помещена в корзину'
        return 'У вас нет доступа к данной заметке'

    def retrieve(self, request_user: User):
        if (self.note.user == request_user) or request_user.is_superuser:
            self.note.retrieve()
            return f'Заметка "{self.note.title}" восстановлена'
        return 'У вас нет доступа к данной заметке'

    def download(self, extension, request_user: User):
        if (self.note.user == request_user) or request_user.is_superuser:
            return self.note.download(extension)
        return False

    class Meta:
        abstract = True


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


class State(ABC):
    @abstractmethod
    def edit(self, note, name=None, text=None):
        pass

    @abstractmethod
    def save(self, note):
        pass

    @abstractmethod
    def download(self, note):
        pass

    @abstractmethod
    def delete(self, note):
        pass

    @abstractmethod
    def show(self, note):
        pass


class Stable(State):
    def edit(self, note, name=None, text=None):
        note._state = Editable()
        print(note.strategy.translate_from_rus('Заметка переведена в режим редактирования.'))

    def save(self, note):
        print(note.strategy.translate_from_rus('Заметка не была изменена, состояние не меняется.'))

    def download(self, note):
        note._state = Downloadable()
        print(note.strategy.translate_from_rus('Выберите место для загрузки заметки.'))

    def delete(self, note):
        note._state = InBasket()
        print(note.strategy.translate_from_rus('Заметка помещена в корзину.'))

    def show(self, note):
        name = note.strategy.translate_from_rus(note.name)
        text = note.strategy.translate_from_rus(note.text)
        note_word = note.strategy.translate_from_rus('Заметка')
        return f"{note_word} '{name}' (язык отображения {note.strategy}):\n{text}"

    def __str__(self):
        return 'Стабильное состояние'


class Editable(State):
    def edit(self, note, name=None, text=None):
        if name is not None:
            note.name = name
        if text is not None:
            note.text = text
        print(note.strategy.translate_from_rus('Свойства заметки изменены.'))

    def save(self, note):
        note._state = Stable()
        print(note.strategy.translate_from_rus('Изменения заметки сохранены.'))

    def download(self, note):
        print(note.strategy.translate_from_rus('Сохраните заметку перед загрузкой.'))

    def delete(self, note):
        print(note.strategy.translate_from_rus('Сохраните заметку перед удалением.'))

    def show(self, note):
        name = note.strategy.translate_from_rus(note.name)
        text = note.strategy.translate_from_rus("находится в режиме редактирования.")
        note_word = note.strategy.translate_from_rus('Заметка')
        return f"{note_word} '{name}' {text}"

    def __str__(self):
        return 'Состояние редактирования'


class Downloadable(State):
    def edit(self, note, name=None, text=None):
        print(note.strategy.translate_from_rus('Заметка не может быть изменена при загрузке.'))

    def save(self, note):
        note._state = Stable()
        print(note.strategy.translate_from_rus('Заметка была сохранена на компьютере.'))

    def download(self, note):
        print(note.strategy.translate_from_rus('Вы уже загружаете данную заметку.'))

    def delete(self, note):
        note._state = Stable()
        print(note.strategy.translate_from_rus('Загрузка была отменена.'))

    def show(self, note):
        name = note.strategy.translate_from_rus(note.name)
        text = note.strategy.translate_from_rus("находится в режиме загрузки.")
        note_word = note.strategy.translate_from_rus('Заметка')
        return f"{note_word} '{name}' {text}"

    def __str__(self):
        return 'Состояние загрузки'


class InBasket(State):
    def edit(self, note, name=None, text=None):
        print(note.strategy.translate_from_rus('Заметка не может быть изменена из корзины.'))

    def save(self, note):
        note._state = Stable()
        print(note.strategy.translate_from_rus('Заметка была восстановлена.'))

    def download(self, note):
        print(note.strategy.translate_from_rus('Заметка не может быть загружена из корзины.'))

    def delete(self, note):
        del note
        print('Заметка удалена без возможности восстановления.')

    def show(self, note):
        name = note.strategy.translate_from_rus(note.name)
        text = note.strategy.translate_from_rus("находится в корзине.")
        note_word = note.strategy.translate_from_rus('Заметка')
        return f"{note_word} '{name}' {text}"

    def __str__(self):
        return 'Заметка в корзине'


class Strategy(ABC):
    @abstractmethod
    def translate_from_rus(self, text):
        pass


class RussianText(Strategy):
    def translate_from_rus(self, text):
        return text

    def __str__(self):
        return 'Русский'


class EnglishText(Strategy):
    def translate_from_rus(self, text):
        translator = Translator(from_lang='ru', to_lang='en')
        eng_text = translator.translate(text)
        return eng_text

    def __str__(self):
        return 'English'


class GermanText(Strategy):
    def translate_from_rus(self, text):
        translator = Translator(from_lang='ru', to_lang='de')
        ger_text = translator.translate(text)
        return ger_text

    def __str__(self):
        return 'Deutsch'


class StatedNote:
    def __init__(self, name, text, state: State = Stable(), strategy: Strategy = RussianText()):
        self.name = name
        self.text = text
        self._state = state
        self._strategy = strategy

    def edit(self, name=None, text=None):
        self._state.edit(self, name, text)

    def save(self):
        self._state.save(self)

    def download(self):
        self._state.download(self)

    def delete(self):
        self._state.delete(self)

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def __str__(self):
        return self._state.show(self)
