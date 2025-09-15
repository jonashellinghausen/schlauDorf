import unittest
from datetime import datetime, timedelta

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

    def test_unpublished_news_hidden(self):
        hidden = News(title='Hidden News', content='Secret', is_published=False)
        db.session.add(hidden)
        db.session.commit()

        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Hidden News', response.data)

    def test_events_ordered_by_start_date(self):
        earlier = Event(
            title='Earlier Event',
            start_date=datetime.utcnow() - timedelta(days=1),
            description='First',
        )
        later = Event(
            title='Later Event',
            start_date=datetime.utcnow() + timedelta(days=1),
            description='Last',
        )
        db.session.add_all([earlier, later])
        db.session.commit()

        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertTrue(
            data.index(b'Earlier Event') < data.index(b'Test Event') < data.index(b'Later Event')
        )


if __name__ == '__main__':
    unittest.main()
