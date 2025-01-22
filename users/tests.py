import time

from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy

from profitpages.models import Publication, Subscription
from users.models import User


class UserLoginViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            phone=88005553535,
            email='myemail@yandex.ru',
            first_name='Test',
            last_name='Testov')
        self.client = Client()
        password = 'testpassword'
        self.user.set_password(password)

    def test_login(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('users:login'), {
            'phone': '88005553535',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)


class SMSVerificationViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_sms_verification_view(self):
        response = self.client.post(reverse('users:sms_verification'), {'sms': '1111'})
        self.client.session['sms'] = '1111'
        self.client.session['password1'] = 'testpassword'
        self.client.session['email'] = 'test@example.com'
        self.client.session['first_name'] = 'Test'
        self.client.session['last_name'] = 'User'
        self.assertEqual(response.status_code, 200)


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_view(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('users:register'), {
            'phone': '1234567890',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpassword',
            'password2': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('phone', response.context['form'].fields)
        self.assertIn('email', response.context['form'].fields)
        self.assertIn('first_name', response.context['form'].fields)
        self.assertIn('last_name', response.context['form'].fields)
        self.assertIn('password1', response.context['form'].fields)
        self.assertIn('password2', response.context['form'].fields)

        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('users:sms_verification'), {'sms': '1111'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login'))
        self.assertTrue(User.objects.filter(email='test@example.com').exists())


class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            phone=88005553535,
            email='myemail@yandex.ru',
            first_name='Test',
            last_name='Testov'
        )
        self.publication = Publication.objects.create(
            user=self.user,
            updated_at='2012-01-01 00:00:00',
            link='test-link'
        )
        Subscription.objects.create(
            user=self.user
        )

    def test_profile_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('users:profile', args={self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

        context = response.context_data
        self.assertEqual(context['publications'].count(), 1)
        self.assertEqual(context['last_publications'].count(), 1)
        self.assertEqual(context['subscribe_hide'], True)


class ProfileUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            phone=88005553535,
            email='hoodnika213@yandex.ru',
            first_name='Test',
            last_name='Testov'
        )

        self.client.force_login(self.user)

    def test_profile_update_view(self):
        data = {
            'first_name': 'Updated',
            'last_name': 'UPDATED_LAST_NAME',
            'submit': True
        }
        response = self.client.post(reverse('users:profile_update', kwargs={'pk': self.user.pk}), data)
        self.assertEqual(response.status_code, 200)