from django.test import TestCase
from django.test.client import Client
import os
from coach.models import User, Speech, Recording
import Cookie


class SystemTest(TestCase):

    def setup(self):
        """Set up token for User Temp Temp with email tempt3699@gmail.com"""
        self.token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjM4Y2FjZjM3ZjUyOWQ4YzM2ZDBlNmJkYzU5OTNlNWQ3Njk1ZDg5NzgifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiaWF0IjoxNDc5Nzg4MjQ3LCJleHAiOjE0Nzk3OTE4NDcsImF0X2hhc2giOiJiRUpOSXNWMGx3Z1E1bGlKVGd6XzJRIiwiYXVkIjoiODI5NjExMTcwNTE5LXUyZnU4bmlzOXVubTRudmxtZmRjdWhpcW9kOXJzYnVoLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTEzMTE3ODQ4ODc2MDUxNjA5Nzk5IiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF6cCI6IjgyOTYxMTE3MDUxOS11MmZ1OG5pczl1bm00bnZsbWZkY3VoaXFvZDlyc2J1aC5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImVtYWlsIjoidGVtcHQzNjk5QGdtYWlsLmNvbSIsIm5hbWUiOiJUZW1wIFRlbXAiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tLy12SFo2eGIybTZTOC9BQUFBQUFBQUFBSS9BQUFBQUFBQUFBQS9BRU1PWVNEcWwyQ2lKaXJNdmNLam1iTnV6RGktRnJYQWNnL3M5Ni1jL3Bob3RvLmpwZyIsImdpdmVuX25hbWUiOiJUZW1wIiwiZmFtaWx5X25hbWUiOiJUZW1wIiwibG9jYWxlIjoiZW4ifQ.MZZD2Jt04sznKHvSEy_X9Iv2Q6d4_DhHKY2uh61r5741C2DMjMFd1G1EOtSheq-EDM9nKPvWkNjUgdtTmv_Je_4fL9z0tXeczceFHNnQF_ZXqldIdcSWFnHkAs68K_zmSFAhY70gEE4XxH3vZaH9sQWWgDdpZuZT5kJXuIXqWpDe_WvAwHa13BdfXDHZo7Ef-em8V5rLEjLAOEilUHVA8BdLhr-0nl2ycV9X0PDn09aPfGRqmGhOVMgWOL0P76zWhPTu_AdBTF7l9x5Dm3za2vl77G8LebUhkmr18FZ-KucaQbO-7o58OmLfSrl0J6-84k0SS764aJWnK9fodR2Qxg"

    def test_index(self):
        """Test loading index page"""
        client = Client()
        # first check that the client can load the index page
        response = client.get('/', secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertRegexpMatches(response.content, '<\!doctype html>',
                                 'index does not contain an html doctype.')
        # assuming style/behavior is correct (as its hard to test from
        # django as the site may change content)

    def test_upload(self):
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

    def test_result_handle_bad_token(self):
        """Test if result page redirects when user is not logged in"""
        client = Client()
        response = client.get('/result', secure=True, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_result_bad_token(self):
        """Test if a bad token is handled"""
        client = Client()
        cookie = Cookie.SimpleCookie()
        cookie['id_token'] = 'I am not a token'
        client.cookies = cookie
        response = client.get('/result', secure=True)
        self.assertEqual(response.status_code, 400)
        self.assertRegexpMatches(response.content,
                                 'Invalid id token: that\'s a no no',
                                 'Did not display error message')

    def test_result_user_not_exit(self):
        """Test if user does not exist scenario is handled"""
        self.setup()
        client = Client()
        cookie = Cookie.SimpleCookie()
        cookie['id_token'] = self.token
        client.cookies = cookie
        response = client.get('/result', secure=True)
        self.assertEqual(response.status_code, 400)
        self.assertRegexpMatches(response.content,
                                 'User does not exist: how did you get here?',
                                 'Did not display error message')

    def test_result_no_rid_provided(self):
        """Test if rid not provided scenario is handled"""
        self.setup()
        client = Client()
        cookie = Cookie.SimpleCookie()
        cookie['id_token'] = self.token
        user = User(name="Temp Temp", email="tempt3699@gmail.com")
        user.save()
        client.cookies = cookie
        response = client.get('/result', secure=True)
        self.assertEqual(response.status_code, 400)
        self.assertRegexpMatches(response.content,
                                 'No ID was provided',
                                 'Did not display error message')
        user.delete()

    def test_result_access_others_recording(self):
        """Test if user is not allowed to access other person's recording"""
        self.setup()
        client = Client()
        cookie = Cookie.SimpleCookie()
        cookie['id_token'] = self.token
        user = User(name="Temp Temp", email="tempt3699@gmail.com")
        user.save()
        client.cookies = cookie
        response = client.get('/result?rid=100000', secure=True)
        self.assertEqual(response.status_code, 400)
        self.assertRegexpMatches(response.content,
                                 'Permission denied: how did you get here?',
                                 'Did not display error message')
        user.delete()

    def test_result_access_recording_success(self):
        """Test if user can access one's own recording"""
        self.setup()
        client = Client()
        cookie = Cookie.SimpleCookie()
        cookie['id_token'] = self.token
        user = User(name="Temp Temp", email="tempt3699@gmail.com")
        user.save()
        speech = Speech(user=user, name="Speech1")
        speech.save()
        audio_dir = "dummy/dir"
        speech = Speech.objects.get(name="Speech1")
        recording = Recording.create(
            speech=speech, audio_dir=audio_dir, transcript=[])
        recording.save()
        id = recording.id
        client.cookies = cookie
        response = client.get('/result?rid=' + str(id), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertRegexpMatches(response.content, '<\!doctype html>',
                                 'result does not contain an html doctype.')
        user.delete()
