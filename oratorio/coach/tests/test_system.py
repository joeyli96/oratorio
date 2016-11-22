from django.test import TestCase
from django.test.client import Client
import os
from coach.models import Recording
import Cookie


class SystemTest(TestCase):

    def test_index(self):
        client = Client()
        # first check that the client can load the index page
        response = client.get('/', secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertRegexpMatches(response.content, '<\!doctype html>',
                                 'index does not contain an html doctype.')
        # assuming style/behavior is correct (as its hard to test from
        # django as the site may change content)

    def test_upload(self):
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
        client = Client()
        response = client.get('/upload', secure=True)
        self.assertEqual(response.status_code, 302,
                         'Loading upload from a browser does not redirect')

    def test_result_handle_bad_token(self):
        client = Client()
        response = client.get('/result', secure=True, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_result_bad_token(self):
        client = Client()
        cookie = Cookie.SimpleCookie()
        cookie['id_token'] = 'I am not a token'
        client.cookies = cookie
        response = client.get('/result', secure=True)
        self.assertEqual(response.status_code, 400)
        self.assertRegexpMatches(response.content,
                                 'Invalid id token: that\'s a no no',
                                 'Did not display error message')
