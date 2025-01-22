from django.test import TestCase, LiveServerTestCase, TransactionTestCase
from django.urls import reverse

from profitpages.models import Publication, Subscription
from users.models import User


class PublicationListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            phone=88005553535,
            email='myemail@yandex.ru',
            first_name='Test',
            last_name='Testov'
        )
        self.user.set_password('testpassword')
        self.publication1 = Publication.objects.create(title='Publication 1', user=self.user, link='publication-1')
        self.publication2 = Publication.objects.create(title='Publication 2', user=self.user, link='publication-2')
        self.publication3 = Publication.objects.create(title='Publication 3', user=self.user, link='publication-3')

    def test_get_queryset_without_subscription(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('profitpages:main'))
        self.assertEqual(list(response.context['publications']),
                         [self.publication3, self.publication2, self.publication1])

    def test_get_context_data_without_subscription(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('profitpages:main'))
        self.assertEqual(response.context['carousel_middle_text'],
                         'Оформите подписку, для доступа к большей библиотеке публикаций')
        self.assertFalse(response.context['carousel_middle_text_hide'])


class PublicationSearchViewTestCase(LiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create(
            phone=88005553535,
            email='myemail@yandex.ru',
            first_name='Test',
            last_name='Testov'
        )
        self.user.set_password('testpassword')
        self.publication1 = Publication.objects.create(title='Publication 1', user=self.user, link='publication-1')
        self.publication2 = Publication.objects.create(title='Publication 2', user=self.user, link='publication-2')
        self.publication3 = Publication.objects.create(title='Publication 3', user=self.user, link='publication-3')


class PublicationAuthorListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            phone=88005553535,
            email='myemail@yandex.ru',
            first_name='Test',
            last_name='Testov'
        )
        self.author = User.objects.create(
            phone=1111111111,
            email='test@yandex.ru',
            first_name='NeTest',
            last_name='NeTestov'
        )
        self.publication1 = Publication.objects.create(title='Publication 1', user=self.author, link='publication-1')
        self.publication2 = Publication.objects.create(title='Publication 2', user=self.user, link='publication-2')
        self.publication3 = Publication.objects.create(title='Publication 3', user=self.author, link='publication-3')
        self.client.force_login(user=self.user)

    def test_get_queryset(self):
        response = self.client.get(reverse('profitpages:publication_user', kwargs={'pk': self.user.pk}))
        self.assertEqual(list(response.context['publications']), [self.publication3, self.publication1])

    def test_get_context_data(self):
        response = self.client.get(reverse('profitpages:publication_user', kwargs={'pk': self.user.pk}))


class PublicationDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            phone=88005553535,
            email='myemail@yandex.ru',
            first_name='Test',
            last_name='Testov'
        )
        self.publication = Publication.objects.create(title='Test Publication', content='Test content', user=self.user,
                                                      link='test-publication')

    def test_get_publication_detail(self):
        url = reverse('profitpages:publication_detail', kwargs={'link': self.publication.link})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.publication.title)
        self.assertContains(response, self.publication.content)


class PublicationCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            phone=88005553535,
            email='myemail@yandex.ru',
            first_name='Test',
            last_name='Testov'
        )
        self.client.force_login(user=self.user)

    def test_create_publication(self):
        form_data = {
            'title': 'Test Publication',
            'content': 'Test content',
            'link': 'test publication',
            'description': 'Test description'
        }
        url = reverse('profitpages:publication_create')
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertEqual(Publication.objects.count(), 1)
        publication = Publication.objects.first()
        self.assertEqual(publication.title, form_data['title'])
        self.assertEqual(publication.content, form_data['content'])
        self.assertEqual(publication.owner, self.user)


class PublicationUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            phone=88005553535,
            email='myemail@yandex.ru',
            first_name='Test',
            last_name='Testov'
        )
        self.client.force_login(user=self.user)
        self.publication = Publication.objects.create(title='Test Publication', content='Test content', user=self.user, link='test_publication')

    def test_update_publication(self):
        form_data = {
            'title': 'Updated Test Publication',
            'content': 'Updated content',
            'btn_save': 'save'
        }
        url = reverse('profitpages:publication_update', kwargs={'pk': self.publication.pk})
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 200)


class PublicationDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            phone=88005553535,
            email='myemail@yandex.ru',
            first_name='Test',
            last_name='Testov'
        )
        self.client.force_login(user=self.user)
        self.publication = Publication.objects.create(title='Test Publication', content='Test content', user=self.user, link='test_publication')

    def test_delete_publication(self):
        url = reverse('profitpages:publication_delete', kwargs={'pk': self.publication.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertEqual(Publication.objects.count(), 0)