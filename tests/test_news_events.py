import unittest
from datetime import datetime

from app import create_app
from app.extensions import db
from app.models import News, Event
from app.config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class NewsEventsRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        news = News(title='Test News', content='Content', is_published=True)
        event = Event(title='Test Event', start_date=datetime.utcnow(), description='Desc')
        db.session.add_all([news, event])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_news_list(self):
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test News', response.data)

    def test_events_list(self):
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Event', response.data)


if __name__ == '__main__':
    unittest.main()
