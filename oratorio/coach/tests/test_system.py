from django.test import TestCase
from django.test.client import Client
import os
from coach.models import User, Speech, Recording
import Cookie
from coach import utils
from mock import MagicMock


class SystemTest(TestCase):
    def setup_mock(self):
        """Mock out verify_id_token in utils.py to return a dummy result"""
        idinfo_mock = {'name': 'Temp Temp', 'email': 'tempt3699@gmail.com', }
        utils.verify_id_token = MagicMock(return_value = idinfo_mock)

    def get_client_with_token(self):
        """Return a client that holds a cookie with a dummy token for User Temp Temp with email tempt3699@gmail.com"""
        dummy_cookie = Cookie.SimpleCookie()
        dummy_cookie['id_token'] = "dummy_token"
        client = Client()
        client.cookies = dummy_cookie
        return client

    def test_index(self):
        """Test loading index page"""
        client = Client()
        # first check that the client can load the index page
        response = client.get('/', secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<!doctype html>', response.content,
                                 'index does not contain an html doctype.')
        # assuming style/behavior is correct (as its hard to test from
        # django as the site may change content)

    def test_index_logged_in(self):
        """Test loading index page while logged in"""
        self.setup_mock()
        client = self.get_client_with_token()
        response = client.get('/', secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<!doctype html>', response.content, 
                'index does not contain an html doctype.')

    def test_login(self):
        """Test login procedure"""
        self.setup_mock()
        client = self.get_client_with_token()
        response = client.post('/login')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "OK")

    def test_upload_logged_in(self):
        """Test uploading audio while logged in"""
        self.setup_mock()
        client = self.get_client_with_token()
        dir = os.path.join(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))), 'tests/')
        audio = open(os.path.join(dir, 'ObamaOut.wav'), 'rb')
        blob = audio.read()
        user = User(name="Temp Temp", email="tempt3699@gmail.com")
        user.save()
        response = client.post('/upload', data=blob,
                               content_type="audio/wav", secure=True)
        self.assertEqual(response.status_code, 200, response)
        recording = Recording.objects.filter(id=response.content)[0]
        self.assertRegexpMatches(recording.get_transcript_text(),
                                 'we all look great. the end of the Republic has never looked better.',
                                 'Did not transcribe the audio correctly')
        user.delete()

    def test_upload_not_logged_in(self):
        """Test uploading an audio and get transcript back"""
        client = Client()
        dir = os.path.join(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))), 'tests/')
        audio = open(os.path.join(dir, 'ObamaOut.wav'), 'rb')
        blob = audio.read()
        response = client.post('/upload', data=blob,
                               content_type="audio/wav", secure=True)
        self.assertEqual(response.status_code, 200)
        recording = Recording.objects.filter(id=response.content)[0]
        self.assertRegexpMatches(recording.get_transcript_text(),
                                 'we all look great. the end of the Republic has never looked better.',
                                 'Did not transcribe the audio correctly')

    def test_malicious_upload(self):
        """Test uploading maliciously"""
        client = Client()
        response = client.get('/upload', secure=True)
        self.assertEqual(response.status_code, 302,
                         'Loading upload from a browser does not redirect')

    def test_profile_not_logged_in(self):
        """Test if profile redirects to index when not logged in"""
        client = Client()
        response = client.get('/profile', secure=True, follow=True)
        self.assertEqual(response.status_code, 200)
        # Get index page to compare to response
        index_response = client.get('/', secure=True)
        self.assertEqual(response.content, index_response.content)

    def test_profile_logged_in(self):
        """Test if profile works while logged in"""
        self.setup_mock()
        client = self.get_client_with_token()
        user = User(name='Temp Temp', email='tempt3699@gmail.com')
        user.save()
        response = client.get('/profile', secure=True, follow=True)
        user.delete()
        self.assertEqual(response.status_code, 200)
        self.assertIn('<div id="ProfilePanel">', response.content)

    def test_result_not_logged_in(self):
        """Test if result page redirects to index when user is not logged in"""
        client = Client()
        response = client.get('/result?rid=0', secure=True, follow=True)
        self.assertEqual(response.status_code, 200)
        # Get index page to compare to response
        index_response = client.get('/', secure=True)
        self.assertEqual(response.content, index_response.content)

    def test_result_user_not_exist(self):
        """Test if user does not exist scenario is handled"""
        self.setup_mock()
        client = self.get_client_with_token()
        response = client.get('/result?rid=0', secure=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content,
                                 'User does not exist: how did you get here?',
                                 'Did not display error message')

    def test_result_no_rid_provided(self):
        """Test if rid not provided scenario is handled"""
        self.setup_mock()
        client = self.get_client_with_token()
        user = User(name='Temp Temp', email='tempt3699@gmail.com')
        user.save()
        response = client.get('/result', secure=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content,
                                 'No ID was provided',
                                 'Did not display error message')
        user.delete()

    def test_result_access_others_recording(self):
        """Test if user is not allowed to access other person's recording"""
        self.setup_mock()
        client = self.get_client_with_token()
        user = User(name='Temp Temp', email='tempt3699@gmail.com')
        user.save()
        response = client.get('/result?rid=100000', secure=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content,
                                 'Permission denied: how did you get here?',
                                 'Did not display error message')
        user.delete()

    def test_result_access_recording_success(self):
        """Test if user can access one's own recording"""
        self.setup_mock()
        client = self.get_client_with_token()
        user = User(name='Temp Temp', email='tempt3699@gmail.com')
        user.save()
        speech = Speech(user=user, name="Speech1")
        speech.save()
        audio_dir = "dummy/dir"
        speech = Speech.objects.get(name="Speech1")
        recording = Recording.create(
            speech=speech, audio_dir=audio_dir, transcript=[])
        recording.save()
        id = recording.id
        response = client.get('/result?rid=' + str(id), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<!doctype html>', response.content,
                                'result does not contain an html doctype.')
        user.delete()

    def test_userdocs_not_logged_in(self):
        """Test if user can access userdocs even if not logged in"""
        client = Client()
        response = client.get("/userdocs", secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Oratorio is a web-based speech coach. Practise your speech or presentation while recording with Oratorio, and it will provide you powerful feedback by analyzing your speech!', response.content)

    def test_userdocs_logged_in(self):
        """Test if user can access userdocs when logged in, and that sidebar loads past speeches"""
        self.setup_mock()
        client = self.get_client_with_token()
        user = User(name='Temp Temp', email='tempt3699@gmail.com')
        user.save()
        speech = Speech(user=user, name="Speech1")
        speech.save()
        audio_dir = "dummy/dir"
        speech = Speech.objects.get(name="Speech1")
        recording = Recording.create(
            speech=speech, audio_dir=audio_dir, transcript=[])
        recording.save()
        response = client.get("/userdocs", secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<div class="menuItem">', response.content)
        self.assertIn('Oratorio is a web-based speech coach. Practise your speech or presentation while recording with Oratorio, and it will provide you powerful feedback by analyzing your speech!', response.content)
        user.delete()
