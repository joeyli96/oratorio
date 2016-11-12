from django.test import TestCase
from django.test.client import Client
import os

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
        self.assertRegexpMatches(response.content,
            'we all look great. the end of the Republic has never looked better.',
            'Did not transcribe the audio correctly')

    def test_malicious_upload(self):
        client = Client()
        response = client.get('/upload', secure=True)
        self.assertEqual(response.status_code, 302,
                         'Loading upload from a browser does not redirect')