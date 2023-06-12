from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.html import strip_tags

from register.models import ColorPreference, Color
from register.forms import RegisterForm
from register.tokens import account_activation_token


class SignUpTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='non_unique', password='ThisIsStrongPassword',
                                                         email='nonunique@example.com')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct_data(self):
        print("\nMethod: test_correct_data")
        form_data = {'username': 'Arkadii', 'password1': 'ThisIsStrongPassword',
                     'password2': 'ThisIsStrongPassword', 'email': 'unique@example.com'}
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        print("\nMethod: test_invalid_email")
        form_data = {'username': 'Arkadii', 'password1': 'ThisIsStrongPassword',
                     'password2': 'ThisIsStrongPassword', 'email': 'unique.com'}
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        print(strip_tags(form.errors['email']))

    def test_non_unique_username(self):
        print("\nMethod: test_non_unique_username")
        form_data = {'username': 'non_unique', 'password1': 'ThisIsStrongPassword',
                     'password2': 'ThisIsStrongPassword', 'email': 'unique@example.com'}
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        print(strip_tags(form.errors['username']))

    def test_non_unique_email(self):
        print("\nMethod: test_non_unique_email")
        form_data = {'username': 'Arkadii', 'password1': 'ThisIsStrongPassword',
                     'password2': 'ThisIsStrongPassword', 'email': 'nonunique@example.com'}
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        print(strip_tags(form.errors['email']))

    def test_invalid_username(self):
        print("\nMethod: test_invalid_username")
        form_data = {'username': 'Arka#dii', 'password1': 'ThisIsStrongPassword',
                     'password2': 'ThisIsStrongPassword', 'email': 'new_test@example.com'}
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        print(strip_tags(form.errors['username']))

    def test_weak_password(self):
        print("\nMethod: test_weak_password")
        form_data = {'username': 'Arkadii', 'password1': '1234',
                     'password2': '1234', 'email': 'new_test@example.com'}
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        print(strip_tags(form.errors['password2']))

    def test_correct_data_response(self):
        print("\nMethod: test_correct_data_response")
        response = self.client.post('/register/', data={'username': 'Arkadii', 'password1': 'ThisIsStrongPassword',
                                                        'password2': 'ThisIsStrongPassword',
                                                        'email': 'unique@example.com'}, follow=True)
        self.assertContains(response, 'Пожалуйста подтвердите свою электронную почту для завершения '
                                      'регистрации')

    def test_incorrect_data_response(self):
        print("\nMethod: test_incorrect_data_response")
        response = self.client.post('/register/', data={'username': 'Arka#dii', 'password1': 'ThisIsStrongPassword',
                                                        'password2': 'ThisIsStrongPassword',
                                                        'email': 'unique@example.com'}, follow=True)
        self.assertNotContains(response, 'Пожалуйста подтвердите свою электронную почту для завершения '
                                         'регистрации')


class ActivationTest(TestCase):
    def setUp(self):
        self.mock = mock.Mock(pk=4, username='test', email='mock@gmail.com', is_active=False)
        self.mock.get_email_field_name.return_value = 'email'

    def test_wrong_activation_token(self):
        print("\nMethod: test_wrong_activation_token")
        new_mock = mock.Mock(pk=5, username='test1', email='mock1@gmail.com', is_active=False)
        new_mock.get_email_field_name.return_value = 'email'
        token = account_activation_token.make_token(new_mock)
        self.assertFalse(account_activation_token.check_token(self.mock, token))

    def test_correct_activation_token(self):
        print("\nMethod: test_correct_activation_token")
        token = account_activation_token.make_token(self.mock)
        self.assertTrue(account_activation_token.check_token(self.mock, token))

    def test_repeated_activation(self):
        print("\nMethod: test_repeated_activation")
        token = account_activation_token.make_token(self.mock)
        if account_activation_token.check_token(self.mock, token):
            self.mock.is_active = True
        self.assertFalse(account_activation_token.check_token(self.mock, token))


class FlyweightTest(TestCase):
    def setUp(self):
        self.red = Color(name='Красный', hex="#FF000050")
        self.red.save()

        self.green = Color(name='Зеленый', hex="#00FF0090")
        self.green.save()

        self.yellow = Color(name='Желтый', hex="#FFFF0090")
        self.yellow.save()

        self.magenta = Color(name='Фиолетовый', hex="#FF00FF90")
        self.magenta.save()

        self.default = ColorPreference(
            high_importance=self.red,
            medium_importance=self.yellow,
            low_importance=self.green
        )
        self.default.save()
        self.user = get_user_model().objects.create_user(username='non_unique', password='ThisIsStrongPassword',
                                                         email='nonunique@example.com',
                                                         preference=self.default)
        self.user.save()

    def test_default_preference(self):
        print("\nMethod: test_default_preference")
        print(f'Идентификатор стандартной схемы: {self.user.preference.id}')

    def test_same_preference_link(self):
        print("\nMethod: test_same_preference_link")
        new_preference = ColorPreference(high_importance=self.red,
                                         medium_importance=self.yellow,
                                         low_importance=self.green
                                         )
        new_preference.save()
        self.assertEqual(new_preference, self.default)

    def test_same_preference(self):
        print("\nMethod: test_same_preference")
        new_user = get_user_model().objects.create_user(username='Arkadii', password='ThisIsStrongPassword',
                                                        email='unique@example.com',
                                                        preference=ColorPreference(
                                                            high_importance=self.red,
                                                            medium_importance=self.yellow,
                                                            low_importance=self.green
                                                        ))
        new_user.save()
        self.assertEqual(new_user.preference.id, self.user.preference.id)

    def test_new_preference(self):
        print("\nMethod: test_new_preference")
        new_user = get_user_model().objects.create_user(username='Arkadii', password='ThisIsStrongPassword',
                                                        email='unique@example.com',
                                                        preference=ColorPreference(
                                                            high_importance=self.red,
                                                            medium_importance=self.yellow,
                                                            low_importance=self.magenta
                                                        ))
        new_user.save()
        self.assertNotEqual(new_user.preference.id, self.user.preference.id)
