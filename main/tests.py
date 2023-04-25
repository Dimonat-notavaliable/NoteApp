from django.test import TestCase
from django.http import HttpResponse
from main.models import SiteLinks, PDFResponse, TXTResponse, NoteActive, NoteInactive, NoteMediator


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
