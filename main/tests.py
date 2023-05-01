from django.contrib.auth import get_user_model
from django.test import TestCase
from django.http import HttpResponse
from main.models import SiteLinks, PDFResponse, TXTResponse, NoteActive, NoteInactive, NoteMediator, TopicInactive,\
    TopicActive, ActiveCreator, InactiveCreator


class SingletonTest(TestCase):
    def setUp(self):
        self.links = SiteLinks()
        self.links.save()

    def tearDown(self):
        self.links.delete()

    def test_sameness(self):
        print("\nMethod: test_sameness")
        new_links = SiteLinks(telegram='telegram')
        new_links.save()
        self.assertEqual(self.links, new_links)


class MediatorTest(TestCase):
    def setUp(self):
        self.mediator = NoteMediator()

    def test_active_to_inactive(self):
        print("\nMethod: test_active_to_inactive")
        convertible = NoteActive()
        convertible.save()
        converted = self.mediator.convert(convertible)
        print(f'Преобразуемый класс: {type(convertible)}; Полученный класс: {type(converted)}')
        self.assertTrue(isinstance(converted, NoteInactive))

    def test_inactive_to_active(self):
        print("\nMethod: test_inactive_to_active")
        convertible = NoteInactive()
        convertible.save()
        converted = self.mediator.convert(convertible)
        print(f'Преобразуемый класс: {type(convertible)}; Полученный класс: {type(converted)}')
        self.assertTrue(isinstance(converted, NoteActive))


class FabricTest(TestCase):
    def setUp(self):
        self.note = NoteActive(title='Фабрика', text='Проверка фабричного метода')

    def test_txt_factory(self):
        print("\nMethod: test_txt_factory")
        response = TXTResponse()
        print(response.check(self.note))
        self.assertTrue(isinstance(response.factory_method(self.note), HttpResponse))

    def test_pdf_factory(self):
        print("\nMethod: test_pdf_factory")
        response = PDFResponse()
        print(response.check(self.note))
        self.assertTrue(isinstance(response.factory_method(self.note), HttpResponse))


class AbstractFactoryTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='non_unique', password='ThisIsStrongPassword',
                                                         email='nonunique@example.com')
        self.user.save()
        self.topic_data = {'user': self.user, 'title': 'Тема'}
        self.note_data = {'user': self.user, 'title': 'Название', 'text': 'Текст'}

    def tearDown(self):
        self.user.delete()

    def test_inactive_factory(self):
        print("\nMethod: test_inactive_factory")
        factory = InactiveCreator()
        topic = factory.create_topic(self.topic_data)
        note = factory.create_note(self.note_data)
        print(f'Созданы: тема {type(topic)}, заметка {type(note)}')
        self.assertTrue(isinstance(topic, TopicInactive) and isinstance(note, NoteInactive))

    def test_active_factory(self):
        print("\nMethod: test_active_factory")
        factory = ActiveCreator()
        topic = factory.create_topic(self.topic_data)
        note = factory.create_note(self.note_data)
        print(f'Созданы: тема {type(topic)}, заметка {type(note)}')
        self.assertTrue(isinstance(topic, TopicActive) and isinstance(note, NoteActive))
