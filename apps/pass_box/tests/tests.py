from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from model_bakery import baker
from pass_box.models import *

PASSBOX_URL = reverse('pass_box:passes-list')
SHARE_URL = reverse('pass_box:shares-list')
User = get_user_model()


class TestPassViewSetApiPublic(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_pass(self):
        baker.make(PassBox, pass_code='1234')
        response = self.client.get(PASSBOX_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_pass(self):
        pass_code = baker.make(PassBox, pass_code='123')
        response = self.client.get(f'{PASSBOX_URL}{pass_code.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_pass(self):
        pass_code = baker.make(PassBox, pass_code='123')
        response = self.client.post(PASSBOX_URL, pass_code.__dict__)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_pass(self):
        pass_code = baker.make(PassBox, pass_code='123')
        response = self.client.delete(f'{PASSBOX_URL}{pass_code.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_pass(self):
        pass_code = baker.make(PassBox, pass_code='123')
        pass_code.pass_code = '1234'
        response = self.client.put(
            f'{PASSBOX_URL}{pass_code.id}/', pass_code.__dict__)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_shared_with_me(self):
        response = self.client.get(f'{PASSBOX_URL}shared_with_me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPassViewSetApiPrivate(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            'test@gmail.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        self.test_user = User.objects.create_user(
            'test2@gmail.com',
            'testpass2'
        )

    def test_list_pass(self):
        baker.make(PassBox, pass_code='123', owner=self.user, _quantity=5)
        response = self.client.get(PASSBOX_URL)
        # print(response.__dict__)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_owner_pass(self):
        pass_code = baker.make(PassBox, pass_code='123', owner=self.user)
        baker.make(PassBox, pass_code='12345', owner=self.test_user)
        response = self.client.get(f'{PASSBOX_URL}{pass_code.id}/')
        # print(response.__dict__)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_not_owner_pass(self):
        baker.make(PassBox, pass_code='123', owner=self.user)
        pass_code = baker.make(
            PassBox, pass_code='12345', owner=self.test_user)
        response = self.client.get(f'{PASSBOX_URL}{pass_code.id}/')
        # print(response.__dict__)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_pass(self):
        pass_code = baker.make(PassBox, pass_code='123')
        response = self.client.post(PASSBOX_URL, pass_code.__dict__)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_owner_pass(self):
        pass_code = baker.make(PassBox, pass_code='123', owner=self.user)
        pass_code.pass_code = '1234'
        response = self.client.put(
            f'{PASSBOX_URL}{pass_code.id}/', pass_code.__dict__)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_not_owner_pass(self):
        pass_code = baker.make(PassBox, pass_code='123', owner=self.test_user)
        pass_code.pass_code = '1234'
        response = self.client.put(
            f'{PASSBOX_URL}{pass_code.id}/', pass_code.__dict__)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_owner_pass(self):
        pass_code = baker.make(PassBox, pass_code='123', owner=self.user)
        response = self.client.delete(f'{PASSBOX_URL}{pass_code.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_not_owner_pass(self):
        pass_code = baker.make(PassBox, pass_code='123', owner=self.test_user)
        response = self.client.delete(f'{PASSBOX_URL}{pass_code.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestShareViewSetApiPublic(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.test_user = User.objects.create_user(
            'test@gmail.com',
            'testpass'
        )
        self.test_user2 = User.objects.create_user(
            'test2@gmail.com',
            'testpass2'
        )

    def test_list_share(self):
        response = self.client.get(SHARE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrive_share(self):
        pass_code = baker.make(PassBox, pass_code='123', owner=self.test_user)
        share = baker.make(ShareList, pass_code=pass_code)
        response = self.client.get(f'{PASSBOX_URL}{share.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_share(self):
        pass_code = baker.make(
            PassBox, pass_code='12345', owner=self.test_user)
        share = baker.make(ShareList, pass_code=pass_code)
        response = self.client.post(SHARE_URL, share.__dict__)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_share(self):
        pass_code = baker.make(PassBox, pass_code='123', owner=self.test_user)
        share = baker.make(ShareList, pass_code=pass_code,
                           user=self.test_user2)
        share.user = self.test_user
        response = self.client.put(f'{SHARE_URL}{share.id}/', share.__dict__)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_share(self):
        pass_code = baker.make(PassBox, pass_code='123', owner=self.test_user)
        share = baker.make(ShareList, pass_code=pass_code)
        response = self.client.delete(f'{PASSBOX_URL}{share.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestShareViewSetPrivate(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            'test@gmail.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        self.client.force_login(self.user)
        self.user_test = User.objects.create_user(
            'test2@gmail.com',
            'testpass2'
        )
        self.user_test2 = User.objects.create_user(
            'test3@gmail.com',
            'testpass3'
        )

    def test_list_share(self):
        pass_code = baker.make(PassBox, pass_code='1234', owner=self.user)
        baker.make(ShareList, pass_code=pass_code, user=self.user_test)
        response = self.client.get(SHARE_URL)
        # print(response.__dict__)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_share_owner_pass(self):
        pass_code = baker.make(PassBox, pass_code='123', owner=self.user)
        share = {
            'pass_code': pass_code.id,
            'user': self.user_test.id
        }
        response = self.client.post(SHARE_URL, share)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_share_not_owner_pass(self):
        pass_code = baker.make(PassBox, pass_code='123', owner=self.user_test)
        share = {
            'pass_code': pass_code.id,
            'user': self.user.id
        }
        response = self.client.post(SHARE_URL, share)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrive_share_owner_pass(self):
        pass_code = baker.make(PassBox, pass_code='123', owner=self.user)
        share = baker.make(ShareList, pass_code=pass_code)
        response = self.client.get(f'{SHARE_URL}{share.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrive_share_not_owner_pass(self):
        pass_code = baker.make(PassBox, pass_code='123', owner=self.user_test)
        share = baker.make(ShareList, pass_code=pass_code)
        response = self.client.get(f'{SHARE_URL}{share.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_share_owner_pass(self):
        pass_code = baker.make(PassBox, pass_code='123', owner=self.user)
        share = baker.make(ShareList, pass_code=pass_code, user=self.user_test)
        updated_share = {
            'pass_code': pass_code.id,
            'user': self.user_test2.id
        }
        response = self.client.put(f'{SHARE_URL}{share.id}/', updated_share)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_share_not_owner_pass(self):
        pass_code = baker.make(PassBox, pass_code='123', owner=self.user_test)
        share = baker.make(ShareList, pass_code=pass_code,
                           user=self.user_test2)
        updated_share = {
            'pass_code': pass_code.id,
            'user': self.user.id
        }
        response = self.client.put(f'{SHARE_URL}{share.id}/', updated_share)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_share_owner_pass(self):
        pass_code = baker.make(PassBox, pass_code='123', owner=self.user)
        share = baker.make(ShareList, pass_code=pass_code, user=self.user_test)
        response = self.client.delete(f'{SHARE_URL}{share.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_share_not_owner_pass(self):
        pass_code = baker.make(PassBox, pass_code='123', owner=self.user_test)
        share = baker.make(ShareList, pass_code=pass_code,
                           user=self.user_test2)
        response = self.client.delete(f'{SHARE_URL}{share.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
