import json

from .BaseCase import BaseCase


class TestGetUsers(BaseCase):

    # def test_empty_response(self):
    #     response = self.app.get('/api/users')
    #     self.assertListEqual(response.json, [])
    #     self.assertEqual(response.status_code, 200)

    def test_user_response(self):
        # Given
        username = "Saravanan"
        password = "@123"
        user_payload = json.dumps({
            "username": username,
            "password": password
        })

        response = self.app.post(
            'http://127.0.0.1:5000/auth', headers={"Content-Type": "application/json"}, data=user_payload)
        login_token = response.json["access_token"]

        users_payload = {
            "_id": "u001",
            "name": "Testing123",
            "email": "Testing123@gmail.com",
            "mealplanid": "M1",
            "feedbackid": "F1"
        }
        response = self.app.post('http://localhost:5000/users',
                                 headers={"Content-Type": "application/json",
                                          "Authorization": f"jwt {login_token}"},
                                 data=json.dumps(users_payload))

        # When
        response = self.app.get('http://localhost:5000/users')
        added_user = response.json[0]

        # Then
        self.assertEqual(users_payload['name'], added_user['name'])
        self.assertEqual(users_payload['email'], added_user['email'])
        self.assertEqual(users_payload['mealplanid'], added_user['mealplanid'])
        self.assertEqual(users_payload['feedbackid'], added_user['feedbackid'])
        self.assertEqual(username, added_user['name']['_id'])
        self.assertEqual(200, response.status_code)
