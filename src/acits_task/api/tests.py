import datetime

from django.test import TestCase, Client, LiveServerTestCase
import copy

from django.utils import timezone

# from pprint import pprint
# from .models import Build, CustomUser


GET_FLATS = \
    [{'build': {'address': 'Address 1',
                'description': 'Descr 1',
                'id': 1,
                'name': 'build 1'},
    'created_at': '2021-10-26T08:10:52.307000Z',
    'flat_rooms': [{'description': 'DESCR',
                    'flat': 1,
                    'flat_attributes': [{'attribute': 1, 'count': 2, 'id': 1},
                                        {'attribute': 1, 'count': 1, 'id': 2}],
                    'id': 1,
                    'type': 'BEDROOM'},
                    {'description': 'descr 2',
                    'flat': 1,
                    'flat_attributes': [],
                    'id': 2,
                    'type': 'GUESTROOM'}],
    'id': 1,
    'owner': 11,
    'price': 10.0,
    'room_count': 2,
    'type': 'TYPE1',
    'updated_at': '2021-10-27T15:07:34.939000Z'},
    {'build': {'address': 'Address 1',
                'description': 'Descr 1',
                'id': 1,
                'name': 'build 1'},
    'created_at': '2021-10-26T08:19:39.751000Z',
    'flat_rooms': [{'description': 'Descr 2',
                    'flat': 2,
                    'flat_attributes': [],
                    'id': 3,
                    'type': 'BEDROOM'}],
    'id': 2,
    'owner': 11,
    'price': 100.0,
    'room_count': 4,
    'type': 'kjkj',
    'updated_at': '2021-10-26T08:19:39.751000Z'}]

FLAT_DATA = {
    'build': 1, 
    'flat_rooms': [
        {'type': 'BEDROOM', 'description': 'DESCR', 
         'flat_attributes': [{'attribute': 1, 'count': 10},
                             {'attribute': 2, 'count': 1}]
        }, 
        {'type': 'GUESTROOM', 'description': 'descr 2',
         'flat_attributes': [{'attribute': 1, 'count': 2},
                             {'attribute': 2, 'count': 5}]
        }
    ], 
    'type': 'TYPE1', 
    'price': 15.0, 
    'room_count': 1
    }

TEST_DATA = {
    'users': [
        {
            'username': 'test10',
            'password': '!Q2w3e4r5t6y',
            'status': 'OWNER',
        },
        {
            'username': 'test2',
            'password': 'SomePA234$',
            'status': 'RENTER',
        },
        {
            'username': 'test3',
            'password': '!Q2w3e4r5t6y',
            'status': 'OWNER',
        },
        {
            'username': 'test4',
            'password': '!Q2w3e4r5t6y',
            'status': 'RENTER',
        },
    ]

}

class ApiTests(LiveServerTestCase):

    fixtures = ['fixtures/dump.json',]
    def get_access_token(self, username, password):
        return self.client.post('/api/v1/auth/token/', {'username': username, 'password': password}, 
                                content_type='application/json').json()['access']

    
    def setUp(self):
        self.client = Client()


    def test_register(self):
        user = {'username': 'newuser', 'password': '@3dkjkjWWD', 'status': 'OWNER'}
        response = self.client.post('/api/v1/register/', user, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('user', response.json().keys())
    
    def test_login(self):
        user_credentials = {'username': 'test1', 'password': '!Q2w3e4r5t6y'}
        response = self.client.post('/api/v1/auth/token/', user_credentials, content_type='application/json')
        self.assertIn('access', response.json().keys())

    def test_get_user(self):
        for user in TEST_DATA['users'][-2:]:
            token = self.get_access_token(user['username'], user['password'])
            response = self.client.get('/api/v1/users/', **{'HTTP_AUTHORIZATION': 'Bearer {}'.format(token)})
            self.assertEqual(response.status_code, 200)
            statuses = set([user['status'] for user in response.json()])

            if user['status'] == 'OWNER':
                self.assertEqual(statuses, {'RENTER'})
            else:
                self.assertEqual(statuses, {'OWNER'})

    def test_get_flat(self):
        user = {'username': 'test1', 'password': '!Q2w3e4r5t6y'}
        token = self.get_access_token(user['username'], user['password'])
        response = self.client.get('/api/v1/flats/', **{'HTTP_AUTHORIZATION': 'Bearer {}'.format(token)})
        self.assertEqual(response.status_code, 200)
        self.maxDiff = None
        self.assertListEqual(response.json(), GET_FLATS)

    def test_create_flat(self):
        user = {'username': 'test2', 'password': '!Q2w3e4r5t6y'}
        token = self.get_access_token(user['username'], user['password'])
        response = self.client.post('/api/v1/flats/', FLAT_DATA, **{'HTTP_AUTHORIZATION': 'Bearer {}'.format(token)}, content_type='application/json')
        self.assertEqual(response.status_code, 201,response.json())
        self.maxDiff = None
        self.assertIn('build', response.json().keys())

    def test_update_flat(self):
        user = {'username': 'test2', 'password': '!Q2w3e4r5t6y'}
        token = self.get_access_token(user['username'], user['password'])
        response = self.client.post('/api/v1/flats/', FLAT_DATA, **{'HTTP_AUTHORIZATION': 'Bearer {}'.format(token)}, content_type='application/json')
        UPDATE_FLAT_DATA = copy.deepcopy(FLAT_DATA)
        flat_id = response.json()['id']
        UPDATE_FLAT_DATA['id'] = flat_id
        UPDATE_FLAT_DATA['flat_rooms'] = [{'type': 'BEDROOM', 'description': 'DESCR', 
                                           'flat_attributes': [{'attribute': 1, 'count': 2}, 
                                                               {'attribute': 2, 'count': 1}
                                        ]}]
        response = self.client.put(f'/api/v1/flats/{flat_id}/', UPDATE_FLAT_DATA, **{'HTTP_AUTHORIZATION': 'Bearer {}'.format(token)}, content_type='application/json')
        self.assertEqual(response.status_code, 200,response.json())
        self.assertIn('build', response.json().keys())

    def test_get_order(self):
        user = {'username': 'test1', 'password': '!Q2w3e4r5t6y'}
        token = self.get_access_token(user['username'], user['password'])
        response = self.client.get('/api/v1/order/', **{'HTTP_AUTHORIZATION': 'Bearer {}'.format(token)}, content_type='application/json')
        self.assertEqual(response.status_code, 200,response.json())
    
    def test_create_delete_order(self):
        user = {'username': 'test1', 'password': '!Q2w3e4r5t6y'}
        ORDER_DATA = {'id': 2, 'date_from': '2021-10-28', 'date_to': '2021-10-29', 'created_at': '2021-10-28T04:56:37.497000Z', 
                      'updated_at': '2021-10-28T04:56:37.497000Z', 'total_price': 333.0, 'flat': 2}
        token = self.get_access_token(user['username'], user['password'])
        response = self.client.post('/api/v1/order/', ORDER_DATA, **{'HTTP_AUTHORIZATION': 'Bearer {}'.format(token)}, content_type='application/json')
        self.assertEqual(response.status_code, 201,response.json())
        self.assertEqual(response.json()['flat'], ORDER_DATA['flat'],response.json())
        order_id = response.json()['id']
        response = self.client.delete(f'/api/v1/order/{order_id}/', **{'HTTP_AUTHORIZATION': 'Bearer {}'.format(token)}, content_type='application/json')
        self.assertEqual(response.status_code, 204)

    def test_update_order(self):
        user = {'username': 'test1', 'password': '!Q2w3e4r5t6y'}
        token = self.get_access_token(user['username'], user['password'])
        response = self.client.get('/api/v1/order/', **{'HTTP_AUTHORIZATION': 'Bearer {}'.format(token)}, content_type='application/json')
        order = response.json()[0]
        order['date_to'] = (timezone.now() + datetime.timedelta(days=10)).date()
        response = self.client.put(f'/api/v1/order/{order["id"]}/', order, **{'HTTP_AUTHORIZATION': 'Bearer {}'.format(token)}, content_type='application/json')
        self.assertEqual(response.status_code, 200,response.json())
        self.assertEqual(response.json()['date_to'], str(order['date_to']))