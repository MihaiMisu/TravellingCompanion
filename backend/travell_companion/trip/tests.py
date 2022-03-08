import pdb

from rest_framework.test import APITestCase

from datetime import datetime
from uuid import uuid4
from json import dumps

from .models import Trip, User


class TestTripAPI(APITestCase):
    ALL_TRIPS_DETAILS_URL = '/trip/detail/'
    SINGLE_TRIP_DETAILS_URL = '/trip/detail/{trip_id}'
    CREATE_TRIP_URL = '/trip/manage'
    UPDATE_PUT_TRIP_URL = '/trip/manage/{trip_id}'

    @classmethod
    def setUpClass(cls):
        u1 = User.objects.create(name='MockUser1', email='mock1@email.com')
        u2 = User.objects.create(name='MockUser2', email='mock2@email.com')
        t1 = Trip.objects.create(
            name='MockTrip1',
            owner_id=u1,
            starting_time=datetime.now(),
            duration=2,
            cost_estimation=3.14,
            description='MockTripDesc'
        )
        t2 = Trip.objects.create(
            name='MockTrip2',
            owner_id=u1,
            starting_time=datetime.now(),
            duration=20,
            cost_estimation=30.104,
            description='MockTripDesc2'
        )

        cls.users = [u1, u2]
        cls.trips = [t1, t2]

    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_all_trips_details(self):
        resp = self.client.get(self.ALL_TRIPS_DETAILS_URL)
        res_body = resp.json()

        for trip in res_body['success']:
            trip['starting_time'] = trip['starting_time'][:19]
            trip['created_at'] = trip['created_at'][:19]
            trip['updated_at'] = trip['updated_at'][:19]

        expected_json = {
            'success': [{
                    'trip_id': str(self.trips[0].trip_id),
                    'name': 'MockTrip1',
                    'owner_id_id': str(self.users[0].user_id),
                    'starting_time': self.trips[0].starting_time.isoformat()[:19],
                    'duration': 2,
                    'cost_estimation': 3.14,
                    'description': 'MockTripDesc',
                    'created_at': self.trips[0].created_at.isoformat()[:19],
                    'updated_at': self.trips[0].updated_at.isoformat()[:19]
                },
                {
                    'trip_id': str(self.trips[1].trip_id),
                    'name': 'MockTrip2',
                    'owner_id_id': str(self.users[0].user_id),
                    'starting_time': self.trips[1].starting_time.isoformat()[:19],
                    'duration': 20,
                    'cost_estimation': 30.104,
                    'description': 'MockTripDesc2',
                    'created_at': self.trips[1].created_at.isoformat()[:19],
                    'updated_at': self.trips[1].updated_at.isoformat()[:19]
                }],
            'error': {}
        }

        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(res_body, expected_json)

    def test_get_single_trip_details(self):
        resp = self.client.get(self.SINGLE_TRIP_DETAILS_URL.format(**{'trip_id': self.trips[0].trip_id}))
        res_body = resp.json()
        res_body['success']['starting_time'] = self.trips[0].starting_time.isoformat()[:19]

        expected_json = {
            'success': {
                'name': 'MockTrip1',
                'owner_id': str(self.users[0].user_id),
                'starting_time': self.trips[0].starting_time.isoformat()[:19],
                'duration': 2,
                'cost_estimation': 3.14,
                'description': 'MockTripDesc',
                'companions': []
            },
            'error': {}
        }

        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(res_body, expected_json)

    def test_trip_not_found(self):
        resp = self.client.get(self.SINGLE_TRIP_DETAILS_URL.format(**{'trip_id': str(uuid4())}))
        res_body = resp.json()

        expected_json = {
            "success": {},
            "error": {
                "message": "Trip not found"
            }
        }

        self.assertEqual(resp.status_code, 404)
        self.assertDictEqual(res_body, expected_json)

    def test_trip_post_fail_missing_mandatory_fields(self):
        payload = {
            "missing_tripName": "Fake",
            "missing_userId1": "628f648b-1274-4ff7-a221-898222bb35bd",
            "missing_startingTime": "2022-12-12T10:10:10",
            "missing_duration": 10,
            "missing_costEstimation": 0.0
        }
        resp = self.client.post(self.CREATE_TRIP_URL, dumps(payload), content_type='application/json')
        resp_body = resp.json()

        expected_json = {
            "error": {
                "tripName": ["This field is required."],
                "userId": ["This field is required."],
                "startingTime": ["This field is required."],
                "duration": ["This field is required."],
                "costEstimation": ["This field is required."]
            }
        }

        self.assertEqual(resp.status_code, 400)
        self.assertDictEqual(resp_body, expected_json)

    def test_trip_post_fail_fields_bad_values(self):
        payload = {
            "tripName": True,
            "userId": "1628f648b-1274-4ff7-a221-898222bb35bd",
            "startingTime": "12022-12-12T10:10:10",
            "duration": 40.1,
            "costEstimation": -3.1,
            "description": True,
            "companions": [1, 2]
        }
        resp = self.client.post(self.CREATE_TRIP_URL, dumps(payload), content_type='application/json')
        resp_body = resp.json()

        expected_json = {
            "error": {
                "tripName": ["Not a valid string."],
                "userId": ["Must be a valid UUID."],
                "startingTime": [
                    "Datetime has wrong format."
                    " Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."
                ],
                "duration": ["A valid integer is required."],
                "description": ["Not a valid string."]
            }
        }

        self.assertEqual(resp.status_code, 400)
        self.assertDictEqual(resp_body, expected_json)

    def test_trip_post_fail_user_not_exist(self):
        payload = {
            "tripName": "fakeTripName",
            "userId": "128f648b-1274-4ff7-a221-898222bb35bd",
            "startingTime": "2022-12-12T10:10:10",
            "duration": 40,
            "costEstimation": 3.1,
            "description": "fake trip description",
            "companions": []
        }
        resp = self.client.post(self.CREATE_TRIP_URL, dumps(payload), content_type='application/json')
        resp_body = resp.json()

        expected_json = {
            "error": {"non_field_errors": ["User ('128f648b-1274-4ff7-a221-898222bb35bd') does not exists"]}
        }

        self.assertEqual(resp.status_code, 400)
        self.assertDictEqual(resp_body, expected_json)

    def test_trip_post_fail_duplicate_user_trip_name(self, ):
        payload = {
            "tripName": self.trips[0].name,
            "userId": str(self.users[0].user_id),
            "startingTime": "2022-12-12T10:10:10",
            "duration": 40,
            "costEstimation": 3.1,
            "description": "fake trip description",
            "companions": []
        }
        resp = self.client.post(self.CREATE_TRIP_URL, dumps(payload), content_type='application/json')
        resp_body = resp.json()

        expected_json = {
            "error": {"non_field_errors": [
                f"A trip with the same name ('{self.trips[0].name}') already exists"
                f" for this user {str(self.users[0].user_id)}."
            ]}
        }

        self.assertEqual(resp.status_code, 400)
        self.assertDictEqual(resp_body, expected_json)

    def test_trip_post_fail_companion_user_not_exist(self):
        fake_companion_id = str(uuid4())
        payload = {
            "tripName": "newTripMock",
            "userId": str(self.users[0].user_id),
            "startingTime": "2022-12-12T10:10:10",
            "duration": 40,
            "costEstimation": 3.1,
            "description": "fake trip description",
            "companions": [fake_companion_id]
        }
        resp = self.client.post(self.CREATE_TRIP_URL, dumps(payload), content_type='application/json')
        resp_body = resp.json()

        expected_json = {
            "error": {"non_field_errors": [
                f"Not existing companions/users: {fake_companion_id}"
            ]}
        }

        self.assertEqual(resp.status_code, 400)
        self.assertDictEqual(resp_body, expected_json)

    def test_trip_post_fail_trip_creator_within_companions_list(self):
        payload = {
            "tripName": "newTripMock",
            "userId": str(self.users[0].user_id),
            "startingTime": "2022-12-12T10:10:10",
            "duration": 40,
            "costEstimation": 3.1,
            "description": "fake trip description",
            "companions": [str(self.users[0].user_id), str(self.users[1].user_id)]
        }
        resp = self.client.post(self.CREATE_TRIP_URL, dumps(payload), content_type='application/json')
        resp_body = resp.json()

        expected_json = {
            "error": {"non_field_errors": ["Trip owner cannot be within the companions list."]}
        }

        self.assertEqual(resp.status_code, 400)
        self.assertDictEqual(resp_body, expected_json)

    def test_trip_post_success_create(self):
        payload = {
            "tripName": "mockTripName",
            "userId": str(self.users[0].user_id),
            "startingTime": "2022-12-12T10:10:10",
            "duration": 40,
            "costEstimation": 3.1,
            "description": "mockDescription",
            "companions": []
        }
        resp = self.client.post(self.CREATE_TRIP_URL, dumps(payload), content_type='application/json')
        resp_body = resp.json()

        expected_json = {
            "success": {
                "tripName": "mockTripName",
                "userId": str(self.users[0].user_id),
                "startingTime": "2022-12-12T10:10:10Z",
                "duration": 40,
                "costEstimation": 3.1,
                "description": "mockDescription",
                "companions": []
            },
            "error": {}
        }

        self.assertEqual(resp.status_code, 201)
        self.assertDictEqual(resp_body, expected_json)

    def test_trip_put_success_create(self):
        payload = {
            "tripName": "mockTripName",
            "userId": str(self.users[0].user_id),
            "startingTime": "2022-12-12T10:10:10",
            "duration": 40,
            "costEstimation": 3.1,
            "description": "mockDescription",
            "companions": []
        }
        resp = self.client.put(
            self.UPDATE_PUT_TRIP_URL.format(**{"trip_id": self.trips[0].trip_id}),
            dumps(payload),
            content_type='application/json'
        )
        resp_body = resp.json()

        expected_json = {
            "success": {
                "tripName": "mockTripName",
                "userId": str(self.users[0].user_id),
                "startingTime": "2022-12-12T10:10:10Z",
                "duration": 40,
                "costEstimation": 3.1,
                "description": "mockDescription",
                "companions": []
            },
            "error": {}
        }

        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp_body, expected_json)
