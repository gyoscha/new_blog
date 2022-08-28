from datetime import datetime

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

from blog_api.models import Note


class TestNoteAPIView(APITestCase):
    """
    TESTS:
    1. Получение пустого списка записей в блоге;
    2. Получение списка записей в блоге;
    3. Создание записи в блоге;
    4. Сортировка по дате создания поста (сначала свежие).
    """
    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test_1', password='1234567')

    def setUp(self) -> None:
        """Перед каждым тестом логиниться"""
        self.client.login(username='test_1', password='1234567')

    @classmethod
    def get_date_create_at(cls):
        now = datetime.now()
        create_at = now.strftime('%d %B %Y - %H:%M')

        return create_at

    def test_empty_list_objects(self):
        url = '/notes/'

        resp = self.client.get(url)

        # Проверка статус кода
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        # Проверка на получение пустого списка
        response_data = resp.data
        expected_data = {
            'count': 0,
            'next': None,
            'previous': None,
            'results': []
        }
        self.assertEqual(expected_data, response_data)

    def test_list_objects(self):
        url = '/notes/'

        note = Note.objects.create(title='Test', note='Test', user_id=1)

        resp = self.client.get(url)

        # Проверка статус кода
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    "id": note.id,
                    "title": "Test",
                    "note": "Test",
                    "create_at": f"{self.get_date_create_at()}",
                    "user": "test_1",
                    "views": 0
                }
            ]
        }

        self.assertDictEqual(expected_data, resp.data)

    def test_login(self):
        resp = self.client.login(username='test_1', password='1234567')

        self.assertTrue(resp)

    def test_create_objects(self):
        url = '/notes/'

        new_title = 'test_title'
        new_note = 'test_message'
        data = {
            'title': new_title,
            'note': new_note,
        }

        resp = self.client.post(url, data=data)

        expected_status_code = status.HTTP_201_CREATED
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            "id": 1,
            "title": "test_title",
            "note": "test_message",
            "create_at": f"{self.get_date_create_at()}",
            "user": "test_1",
            "views": 0
        }

        self.assertTrue(Note.objects.get(pk=1))

        self.assertDictEqual(expected_data, resp.data)

    def test_fresh(self):
        url = '/notes/'

        note_1 = Note.objects.create(title='Test_1', note='Test_1', user_id=1)
        note_2 = Note.objects.create(title='Test_2', note='Test_2', user_id=1)

        resp = self.client.get(url)

        # Проверка статус кода
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    "id": note_2.id,
                    "title": "Test_2",
                    "note": "Test_2",
                    "create_at": f"{self.get_date_create_at()}",
                    "user": "test_1",
                    "views": 0
                },
                {
                    "id": note_1.id,
                    "title": "Test_1",
                    "note": "Test_1",
                    "create_at": f"{self.get_date_create_at()}",
                    "user": "test_1",
                    "views": 0
                }
            ]
        }

        self.assertDictEqual(expected_data, resp.data)


class TestNoteDetailAPIView(APITestCase):
    """
    TESTS:
    1. Получение существующей записи в блоге;
    2. Получение несуществующей записи в блоге;
    3. Обновление существующей записи в блоге;
    4. Обновление несуществующей записи в блоге;
    5. Частичное обновление записи;
    6. Удаление записи;
    7. Обновление или удаление записи другого пользователя;
    8. Получение верного числа просмотров.
    """

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test_1', password='1234567')
        Note.objects.create(title='TEST_title', note='TEST_msg', user_id=1)
        Note.objects.create(title='TEST_title_2', note='TEST_msg_2', user_id=1)

        User.objects.create_user(username='test_2', password='1234567')
        Note.objects.create(title='TEST_title_3', note='TEST_msg_3', user_id=2)

    def setUp(self) -> None:
        """Перед каждым тестом логиниться"""
        self.client.login(username='test_1', password='1234567')

    @classmethod
    def get_date_create_at(cls):
        now = datetime.now()
        create_at = now.strftime('%d %B %Y - %H:%M')

        return create_at

    def test_retrieve_existing_object(self):
        pk = 1
        url = f'/notes/{pk}/'

        resp = self.client.get(url)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            "id": 1,
            "title": "TEST_title",
            "note": "TEST_msg",
            "create_at": f"{self.get_date_create_at()}",
            "user": "test_1",
            "views": 1
        }

        self.assertDictEqual(expected_data, resp.data)

    def test_retrieve_non_existent_object(self):
        pk = 11
        url = f'/notes/{pk}/'

        resp = self.client.get(url)

        expected_status_code = status.HTTP_404_NOT_FOUND
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            "detail": "Not found."
        }

        self.assertDictEqual(expected_data, resp.data)

    def test_update_existing_object(self):
        pk = 1
        url = f'/notes/{pk}/'

        put_data = {
            'title': 'TEST_title_PUT',
            'note': 'TEST_msg_PUT',
        }

        resp = self.client.put(url, put_data)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            "id": 1,
            "title": "TEST_title_PUT",
            "note": "TEST_msg_PUT",
            "create_at": f"{self.get_date_create_at()}",
            "user": "test_1",
            "views": 1
        }

        self.assertDictEqual(expected_data, resp.data)

    def test_update_non_existent_object(self):
        pk = 11
        url = f'/notes/{pk}/'

        put_data = {
            'title': 'TEST_title_PUT',
            'note': 'TEST_msg_PUT',
        }
        resp = self.client.put(url, put_data)

        expected_status_code = status.HTTP_404_NOT_FOUND
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            "detail": "Not found."
        }

        self.assertDictEqual(expected_data, resp.data)

    def test_patch_title(self):
        pk = 2
        url = f'/notes/{pk}/'

        patch_data_1 = {
            'title': 'TEST_title_patch',
        }

        resp = self.client.patch(url, patch_data_1)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            "id": 2,
            "title": "TEST_title_patch",
            "note": "TEST_msg_2",
            "create_at": f"{self.get_date_create_at()}",
            "user": "test_1",
            "views": 1
        }

        self.assertDictEqual(expected_data, resp.data)

    def test_patch_note(self):
        pk = 1
        url = f'/notes/{pk}/'

        patch_data_2 = {
            'note': 'TEST_msg_patch',
        }

        resp = self.client.patch(url, patch_data_2)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            "id": 1,
            "title": "TEST_title",
            "note": "TEST_msg_patch",
            "create_at": f"{self.get_date_create_at()}",
            "user": "test_1",
            "views": 1
        }

        self.assertDictEqual(expected_data, resp.data)

    def test_delete(self):
        pk = 1
        url = f'/notes/{pk}/'

        resp = self.client.delete(url)

        expected_status_code = status.HTTP_204_NO_CONTENT
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = None

        self.assertEqual(expected_data, resp.data)

    def test_not_author_put_or_delete(self):
        pk = 3
        url = f'/notes/{pk}/'

        resp = self.client.get(url)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            "id": 3,
            "title": "TEST_title_3",
            "note": "TEST_msg_3",
            "create_at": f"{self.get_date_create_at()}",
            "user": "test_2",
            "views": 1
        }

        self.assertDictEqual(expected_data, resp.data)

        put_data = {
            'title': 'TEST_title_PUT',
            'note': 'TEST_msg_PUT',
        }
        resp_2 = self.client.put(url, put_data)

        expected_status_code_2 = status.HTTP_403_FORBIDDEN
        self.assertEqual(expected_status_code_2, resp_2.status_code)

        resp_3 = self.client.delete(url)

        expected_status_code_3 = status.HTTP_403_FORBIDDEN
        self.assertEqual(expected_status_code_3, resp_3.status_code)

    def test_views(self):
        pk = 1
        url = f'/notes/{pk}/'

        self.client.get(url)

        self.client.login(username='test_2', password='1234567')

        resp = self.client.get(url)

        expected_data = {
            "id": 1,
            "title": "TEST_title",
            "note": "TEST_msg",
            "create_at": f"{self.get_date_create_at()}",
            "user": "test_1",
            "views": 2
        }

        self.assertDictEqual(expected_data, resp.data)


class TestCreateUserView(APITestCase):
    """
    TESTS:
    1. Регистрация пользователя.
    """
    def test_registration(self):
        url = '/accounts/signup/'

        post_data = {
            'username': 'test_user',
            'password': '1234567',
            'first_name': 'George',
            'last_name': 'Sokolov',
            'email': 'sokolovgeorgy@gmail.com',
        }

        resp = self.client.post(url, post_data)

        expected_status_code = status.HTTP_201_CREATED
        self.assertEqual(expected_status_code, resp.status_code)

        resp_2 = self.client.login(username='test_user', password='1234567')

        self.assertTrue(resp_2)


class TestAccountsAPIView(APITestCase):
    """
    TESTS:
    1. Получение пустого списка пользователей;
    2. Получение списка пользователей;
    3. Сортировка по количеству постов. (чем больше, тем пользователь выше в списке)
    """

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test_1', password='1234567')

        Note.objects.create(title='TEST_title', note='TEST_msg', user_id=1)

    def test_empty_list_users(self):
        url = '/accounts/profiles/'

        resp = self.client.get(url)

        expected_status_code = status.HTTP_403_FORBIDDEN
        self.assertEqual(expected_status_code, resp.status_code)

    def test_list_users(self):
        self.client.login(username='test_1', password='1234567')

        url = '/accounts/profiles/'

        resp = self.client.get(url)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        response_data = resp.data
        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    "user": "test_1",
                    "follow_count": 1,
                    "notes_count": 1,
                },
            ]
        }
        self.assertDictEqual(expected_data, response_data)

    def test_sort_users(self):
        User.objects.create_user(username='test_2', password='1234567')
        Note.objects.create(title='TEST_title_2', note='TEST_msg_2', user_id=2)
        Note.objects.create(title='TEST_title_3', note='TEST_msg_3', user_id=2)

        self.client.login(username='test_1', password='1234567')

        url = '/accounts/profiles/'

        resp = self.client.get(url)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        response_data = resp.data
        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    "user": "test_2",
                    "follow_count": 1,
                    "notes_count": 2,
                },
                {
                    "user": "test_1",
                    "follow_count": 1,
                    "notes_count": 1,
                },
            ]
        }
        self.assertDictEqual(expected_data, response_data)


class TestAccountDetailAPIView(APITestCase):
    """
    TESTS:
    1. Получение существующего пользователя;
    2. Получение несуществующего пользователя;
    3. Подписка на другого пользователя.
    """

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test_1', password='1234567')

        User.objects.create_user(username='test_2', password='1234567')

    def setUp(self) -> None:
        """Перед каждым тестом логиниться"""
        self.client.login(username='test_2', password='1234567')

    def test_retrieve_existing_profile(self):
        pk = 2
        url = f'/accounts/profiles/{pk}/'

        resp = self.client.get(url)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            "user": "test_2",
            "first_name": "",
            "last_name": "",
            "email": "",
            "follow_count": 1,
            "notes_count": 0,
            "follows": [
                2
            ]
        }

        self.assertDictEqual(expected_data, resp.data)

    def test_retrieve_non_existent_profile(self):
        pk = 10
        url = f'/accounts/profiles/{pk}/'

        resp = self.client.get(url)

        expected_status_code = status.HTTP_404_NOT_FOUND
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            "detail": "Not found."
        }

        self.assertDictEqual(expected_data, resp.data)

    def test_follow(self):
        pk = 2
        url = f'/accounts/profiles/{pk}/'

        put_data = {
            "user": "test_2",
            "first_name": "",
            "last_name": "",
            "email": "",
            "follow_count": 2,
            "notes_count": 0,
            "follows": [
                2,
                1
            ]
        }

        resp = self.client.put(url, put_data)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        self.assertDictEqual(put_data, resp.data)


class TestAccountFollowsAPIView(APITestCase):
    """
    TESTS:
    1. Получение подписок пользователя;
    """
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test_1', password='1234567')

        User.objects.create_user(username='test_2', password='1234567')

    def setUp(self) -> None:
        """Перед каждым тестом логиниться"""
        self.client.login(username='test_2', password='1234567')

    def test_follows(self):
        pk = 2
        url_1 = f'/accounts/profiles/{pk}/'
        url_2 = f'/accounts/profiles/{pk}/follows/'

        put_data = {
            "user": "test_2",
            "first_name": "",
            "last_name": "",
            "email": "",
            "follow_count": 2,
            "notes_count": 0,
            "follows": [
                2,
                1
            ]
        }

        self.client.put(url_1, put_data)

        resp = self.client.get(url_2)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            "user": "test_2",
            "follows": [
                {
                    "user": "test_2"
                },
                {
                    "user": "test_1"
                }
            ]
        }

        self.assertDictEqual(expected_data, resp.data)


class TestFeedAPIView(APITestCase):
    """
    TESTS:
    1. Получение ленты постов;
    2. Проверка фильтра на прочитанные посты.
    """

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test_user', password='1234567')
        User.objects.create_user(username='test_user_2', password='1234567')
        User.objects.create_user(username='test_user_3', password='1234567')

        Note.objects.create(title='TEST_title_1', note='TEST_msg_1', user_id=3)
        Note.objects.create(title='TEST_title_2', note='TEST_msg_2', user_id=2)
        Note.objects.create(title='TEST_title_3', note='TEST_msg_3', user_id=1)
        Note.objects.create(title='TEST_title_4', note='TEST_msg_4', user_id=3)

    def setUp(self) -> None:
        """Перед каждым тестом логиниться"""
        self.client.login(username='test_user', password='1234567')
        pk = 1
        url = f'/accounts/profiles/{pk}/'

        put_data = {
            "user": "test_user",
            "first_name": "",
            "last_name": "",
            "email": "",
            "follow_count": 2,
            "notes_count": 1,
            "follows": [
                2,
                3,
            ]
        }

        self.client.put(url, put_data)

    @classmethod
    def get_date_create_at(cls):
        now = datetime.now()
        create_at = now.strftime('%d %B %Y - %H:%M')

        return create_at

    def test_list_feed_objects(self):
        url = '/feed/'

        resp = self.client.get(url)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            'count': 3,
            'next': None,
            'previous': None,
            'results': [
                {
                    "id": 4,
                    "title": "TEST_title_4",
                    "note": "TEST_msg_4",
                    "create_at": f"{self.get_date_create_at()}",
                    "user": "test_user_3",
                    "views": 0
                },
                {
                    "id": 2,
                    "title": "TEST_title_2",
                    "note": "TEST_msg_2",
                    "create_at": f"{self.get_date_create_at()}",
                    "user": "test_user_2",
                    "views": 0
                },
                {
                    "id": 1,
                    "title": "TEST_title_1",
                    "note": "TEST_msg_1",
                    "create_at": f"{self.get_date_create_at()}",
                    "user": "test_user_3",
                    "views": 0
                },
            ]
        }
        self.assertEqual(expected_data, resp.data)

    def test_read_filter(self):
        url_1 = '/feed/2/'
        url_2 = '/feed/4/'
        self.client.get(url_1)
        self.client.get(url_2)

        url_3 = '/feed/?read_posts=1'

        resp = self.client.get(url_3)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    "id": 4,
                    "title": "TEST_title_4",
                    "note": "TEST_msg_4",
                    "create_at": f"{self.get_date_create_at()}",
                    "user": "test_user_3",
                    "views": 1
                },
                {
                    "id": 2,
                    "title": "TEST_title_2",
                    "note": "TEST_msg_2",
                    "create_at": f"{self.get_date_create_at()}",
                    "user": "test_user_2",
                    "views": 1
                },
            ]
        }
        self.assertEqual(expected_data, resp.data)
