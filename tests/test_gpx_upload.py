import io
import os
import shutil
import tempfile
import unittest

import sqlite3
if not hasattr(sqlite3.Connection, "enable_load_extension"):
    try:
        import pysqlite3 as sqlite3  # type: ignore
    except Exception:
        raise unittest.SkipTest("SQLite extension loading is not supported") from None

from app import create_app
from app.config import Config
from app.extensions import db
from app.models.gpx import GPXTrack


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
        track_info = tracks[0]
        self.assertEqual(track_info['name'], 'Sample Track')
        # Geometry should be a GeoJSON LineString
        self.assertEqual(track_info['geometry']['type'], 'LineString')
        self.assertIsNotNone(track_info['distance_km'])
        self.assertIsNotNone(track_info['elevation_gain_m'])

    def test_upload_invalid_extension(self):
        data = {
            'file': (io.BytesIO(b'content'), 'bad.txt'),
        }
        response = self.client.post('/api/gpx/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()

