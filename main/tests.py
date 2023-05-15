from django.contrib.auth import get_user_model
from django.test import TestCase
from django.http import HttpResponse
from main.models import SiteLinks, PDFResponse, TXTResponse, NoteActive, NoteInactive, NoteMediator, NoteProtector


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


class ProxyTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='Allowed', password='ThisIsStrongPassword',
                                                         email='allowed@gmail.com')
        self.intruder = get_user_model().objects.create_user(username='Intruder', password='ThisIsStrongPassword',
                                                         email='intruder@gmail.com')

    def test_delete_protection(self):
        print("\nMethod: test_delete_protection")
        note = NoteActive(id=1, user=self.user, title='Защищенная заметка 1', text='Проверка удаления')
        proxy = NoteProtector(note)
        print(f'Пользователь {self.intruder.username} пытается удалить заметку.'
              f' Ответ: {proxy.place_in_basket(self.intruder)}')
        print(f'Пользователь {self.user.username} пытается удалить заметку.'
              f' Ответ: {proxy.place_in_basket(self.user)}')

    def test_download_protection(self):
        print("\nMethod: test_download_protection")
        note = NoteActive(id=2, user=self.user, title='Защищенная заметка 2', text='Проверка загрузки')
        proxy = NoteProtector(note)
        print(f'Пользователь {self.intruder.username} пытается скачать заметку.'
              f' Ответ: {proxy.download("txt", self.intruder)}')
        print(f'Пользователь {self.user.username} пытается скачать заметку.'
              f' Ответ: {type(proxy.download("txt", self.user))}')

    def test_retrieve_protection(self):
        print("\nMethod: test_retrieve_protection")
        note = NoteInactive(id=3, user=self.user, title='Защищенная заметка 3', text='Проверка восстановления')
        proxy = NoteProtector(note)
        print(f'Пользователь {self.intruder.username} пытается восстановить заметку.'
              f' Ответ: {proxy.retrieve(self.intruder)}')
        print(f'Пользователь {self.user.username} пытается восстановить заметку.'
              f' Ответ: {proxy.retrieve(self.user)}')
