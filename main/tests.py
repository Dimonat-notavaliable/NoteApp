from django.contrib.auth import get_user_model
from django.test import TestCase
from django.http import HttpResponse
from main import models


class SingletonTest(TestCase):
    def setUp(self):
        self.links = models.SiteLinks()
        self.links.save()

    def tearDown(self):
        self.links.delete()

    def test_sameness(self):
        print("\nMethod: test_sameness")
        new_links = models.SiteLinks(telegram='telegram')
        new_links.save()
        self.assertEqual(self.links, new_links)


class MediatorTest(TestCase):
    def setUp(self):
        self.mediator = models.NoteMediator()

    def test_active_to_inactive(self):
        print("\nMethod: test_active_to_inactive")
        convertible = models.NoteActive()
        convertible.save()
        converted = self.mediator.convert(convertible)
        print(f'Преобразуемый класс: {type(convertible)}; Полученный класс: {type(converted)}')
        self.assertTrue(isinstance(converted, models.NoteInactive))

    def test_inactive_to_active(self):
        print("\nMethod: test_inactive_to_active")
        convertible = models.NoteInactive()
        convertible.save()
        converted = self.mediator.convert(convertible)
        print(f'Преобразуемый класс: {type(convertible)}; Полученный класс: {type(converted)}')
        self.assertTrue(isinstance(converted, models.NoteActive))


class FabricTest(TestCase):
    def setUp(self):
        self.note = models.NoteActive(title='Фабрика', text='Проверка фабричного метода')

    def test_txt_factory(self):
        print("\nMethod: test_txt_factory")
        response = models.TXTResponse()
        print(response.check(self.note))
        self.assertTrue(isinstance(response.factory_method(self.note), HttpResponse))

    def test_pdf_factory(self):
        print("\nMethod: test_pdf_factory")
        response = models.PDFResponse()
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
        note = models.NoteActive(id=1, user=self.user, title='Защищенная заметка 1', text='Проверка удаления')
        proxy = models.NoteProtector(note)
        print(f'Пользователь {self.intruder.username} пытается удалить заметку.'
              f' Ответ: {proxy.place_in_basket(self.intruder)}')
        print(f'Пользователь {self.user.username} пытается удалить заметку.'
              f' Ответ: {proxy.place_in_basket(self.user)}')

    def test_download_protection(self):
        print("\nMethod: test_download_protection")
        note = models.NoteActive(id=2, user=self.user, title='Защищенная заметка 2', text='Проверка загрузки')
        proxy = models.NoteProtector(note)
        print(f'Пользователь {self.intruder.username} пытается скачать заметку.'
              f' Ответ: {proxy.download("txt", self.intruder)}')
        print(f'Пользователь {self.user.username} пытается скачать заметку.'
              f' Ответ: {type(proxy.download("txt", self.user))}')

    def test_retrieve_protection(self):
        print("\nMethod: test_retrieve_protection")
        note = models.NoteInactive(id=3, user=self.user, title='Защищенная заметка 3', text='Проверка восстановления')
        proxy = models.NoteProtector(note)
        print(f'Пользователь {self.intruder.username} пытается восстановить заметку.'
              f' Ответ: {proxy.retrieve(self.intruder)}')
        print(f'Пользователь {self.user.username} пытается восстановить заметку.'
              f' Ответ: {proxy.retrieve(self.user)}')


class StateTest(TestCase):
    def setUp(self):

        self.stable_note = models.StatedNote('Стабильная', 'Тестирование стабильной заметки',
                                             state=models.Stable())
        self.editable_note = models.StatedNote('Редактирование', 'Тестирование редактируемой заметки',
                                               state=models.Editable())
        self.downloadable_note = models.StatedNote('Загрузка', 'Тестирование загружаемой заметки',
                                                   state=models.Downloadable())
        self.deleted_note = models.StatedNote('В корзине', 'Тестирование заметки в корзине',
                                              state=models.InBasket())
        self.notes = {
            'stable': self.stable_note,
            'editable': self.editable_note,
            'downloadable': self.downloadable_note,
            'deleted': self.deleted_note
        }

    def test_states_editing(self):
        print("\nMethod: test_states_editing")

        for state in ['stable', 'editable', 'downloadable', 'deleted']:
            print(f'Начальное состояние: {self.notes[state]._state}')
            self.notes[state].edit()
            print(f'Текущее состояние: {self.notes[state]._state}',
                  '-------------------------------------', sep='\n')

    def test_states_saving(self):
        print("\nMethod: test_states_saving")

        for state in ['stable', 'editable', 'downloadable', 'deleted']:
            print(f'Начальное состояние: {self.notes[state]._state}')
            self.notes[state].save()
            print(f'Текущее состояние: {self.notes[state]._state}',
                  '-------------------------------------', sep='\n')

    def test_states_downloading(self):
        print("\nMethod: test_states_downloading")

        for state in ['stable', 'editable', 'downloadable', 'deleted']:
            print(f'Начальное состояние: {self.notes[state]._state}')
            self.notes[state].download()
            print(f'Текущее состояние: {self.notes[state]._state}',
                  '-------------------------------------', sep='\n')

    def test_states_deleting(self):
        print("\nMethod: test_states_deleting")

        for state in ['stable', 'editable', 'downloadable', 'deleted']:
            print(f'Начальное состояние: {self.notes[state]._state}')
            self.notes[state].delete()
            print(f'Текущее состояние: {self.notes[state]._state}',
                  '-------------------------------------', sep='\n')


class StrategyTest(TestCase):
    def setUp(self):
        self.note = models.StatedNote(
            name='Тестирование',
            text='Этот текст должен быть переведен.',
            state=models.Stable()
        )

    def test_rus_strategy(self):
        print("\nMethod: test_rus_strategy")
        print(self.note)

    def test_eng_strategy(self):
        print("\nMethod: test_eng_strategy")
        self.note.strategy = models.EnglishText()
        print(self.note)

    def test_ger_strategy(self):
        print("\nMethod: test_ger_strategy")
        self.note.strategy = models.GermanText()
        print(self.note)
