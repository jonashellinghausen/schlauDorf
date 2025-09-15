import io
import os
import shutil
import sqlite3
import tempfile
import unittest

if not hasattr(sqlite3.Connection, "enable_load_extension"):
    raise unittest.SkipTest("SQLite extension loading is not supported")

from sqlalchemy import event
from sqlalchemy.engine import Engine

from app import create_app
from app.config import Config
from app.extensions import db
from app.models.gpx import GPXTrack


@event.listens_for(Engine, "connect")
def load_spatialite(dbapi_conn, connection_record):
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension("mod_spatialite")


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class GPXUploadTestCase(unittest.TestCase):
    def setUp(self):
        self.upload_folder = tempfile.mkdtemp()
        class ConfigWithUpload(TestConfig):
            UPLOAD_FOLDER = self.upload_folder
        self.app = create_app(ConfigWithUpload)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        shutil.rmtree(self.upload_folder)

    @staticmethod
    def _sample_gpx():
        return b"""<?xml version='1.0' encoding='UTF-8'?>
<gpx version='1.1' creator='test'>
<trk><name>Test</name><trkseg>
<trkpt lat='0' lon='0'><ele>0</ele></trkpt>
<trkpt lat='0' lon='0.001'><ele>1</ele></trkpt>
</trkseg></trk>
</gpx>"""

    def test_upload_gpx_track(self):
        data = {
            'file': (io.BytesIO(self._sample_gpx()), 'track.gpx'),
            'name': 'Sample Track',
        }
        response = self.client.post('/api/gpx/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 201)
        json_data = response.get_json()
        self.assertEqual(json_data['name'], 'Sample Track')
        self.assertEqual(GPXTrack.query.count(), 1)
        track = GPXTrack.query.first()
        self.assertTrue(os.path.exists(os.path.join(self.upload_folder, track.filename)))

        list_resp = self.client.get('/api/gpx/tracks')
        self.assertEqual(list_resp.status_code, 200)
        tracks = list_resp.get_json()
        self.assertEqual(len(tracks), 1)
        self.assertEqual(tracks[0]['name'], 'Sample Track')

    def test_upload_invalid_extension(self):
        data = {
            'file': (io.BytesIO(b'content'), 'bad.txt'),
        }
        response = self.client.post('/api/gpx/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()

