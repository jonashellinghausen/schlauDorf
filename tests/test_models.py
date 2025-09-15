import unittest

from app import create_app
from app.extensions import db
from app.models import User
from app.config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.check_password('testpassword'))
        self.assertEqual(user.username, 'testuser')


if __name__ == '__main__':
    unittest.main()
