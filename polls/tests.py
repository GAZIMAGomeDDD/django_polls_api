from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Poll, Choice
import json

client = APIClient()


class CreatePollTest(TestCase):

    def setUp(self):
        self.valid_payload = {
            "poll_text": "Как настроение?",
            "choices": [
                {"choice_text": "Отлично!"},
                {"choice_text": "Плохо("}
            ]
        }
        self.invalid_payload = {
            "poll_text": "",
            "choices": [
                {"choice_text": ""},
                {"choice_text": ""}
            ]
        }

    def test_create_valid_poll(self):
        response = client.post(
            reverse('createPoll'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_poll(self):
        response = client.post(
            reverse('createPoll'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_createPoll_get_request(self):
        response = client.get(reverse('createPoll'))

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)


class PollTest(TestCase):

    def setUp(self):
        self.poll = Poll.objects.create(poll_text='Какой мессенджер лучше?')
        Choice.objects.bulk_create(
            [
                Choice(choice_text='telegram', poll=self.poll),
                Choice(choice_text='whatsapp', poll=self.poll)
            ]
        )

    def test_poll_valid_response(self):
        response = client.post(
            reverse('poll'),
            data=json.dumps({'poll_id': 1, 'choice_id': 1}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_poll_invalid_response(self):
        response = client.post(
            reverse('poll'),
            data=json.dumps({'poll_id': 4212, 'choice_id': 3233}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_poll_success(self):
        response = client.post(
            reverse('poll'),
            data=json.dumps({'poll_id': 1, 'choice_id': 2}),
            content_type='application/json'
        )

        self.assertDictEqual(response.data, {'success': True})

    def test_poll_not_found(self):
        response = client.post(
            reverse('poll'),
            data=json.dumps({'poll_id': 1212, 'choice_id': 2212}),
            content_type='application/json'
        )

        self.assertDictEqual(response.data, {'detail': 'Not found.'})

    def test_poll_get_request(self):
        response = client.get(reverse('poll'))

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)


class GetResultTest(TestCase):

    def setUp(self):
        self.valid_payload = {
            "poll_text": "Как настроение?",
            "choices": [
                {"choice_text": "Отлично!"},
                {"choice_text": "Плохо("}
            ]
        }
        client.post(
            reverse('createPoll'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

    def test_getResult_valid_response(self):
        response = client.post(
            reverse('getResult'),
            data=json.dumps({'poll_id': 1}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getResult_invalid_response(self):
        response = client.post(
            reverse('getResult'),
            data=json.dumps({'poll_id': 4212}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_getResult_valid_data(self):
        response = client.post(
            reverse('getResult'),
            data=json.dumps({'poll_id': 1}),
            content_type='application/json'
        )

        data = {
            "result": [
                {
                    "id": 1,
                    "poll_id": 1,
                    "choice_text": "Отлично!",
                    "votes": 0
                },
                {
                    "id": 2,
                    "poll_id": 1,
                    "choice_text": "Плохо(",
                    "votes": 0
                }
            ]
        }

        self.assertDictEqual(response.data, data)

    def test_getResult_not_found(self):
        response = client.post(
            reverse('getResult'),
            data=json.dumps({'poll_id': 1212}),
            content_type='application/json'
        )

        self.assertDictEqual(response.data, {'detail': 'Not found.'})

    def test_getResult_get_request(self):
        response = client.get(reverse('getResult'))

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
