import unittest

from app import create_app
from app.extensions import db
from app.models import User, ChatRoom
from app.config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ChatAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        user = User(
            username='tester',
            email='tester@example.com',
            first_name='Test',
            last_name='User',
            is_verified=True,
        )
        user.set_password('password')
        db.session.add(user)
        room = ChatRoom(name='Room 1')
        db.session.add(room)
        db.session.commit()
        self.user = user
        self.room = room

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_post_and_get_messages(self):
        self.client.post(
            '/auth/login',
            data={'username': 'tester', 'password': 'password'},
        )
        url = f'/api/chat/rooms/{self.room.id}/messages'
        response = self.client.post(url, json={'user_id': self.user.id, 'message': 'Hello'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['message'], 'Hello')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['message'], 'Hello')


if __name__ == '__main__':
    unittest.main()
