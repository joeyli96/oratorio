from django.test import TestCase
from ..models import Recording, User, Speech


class RecordingTestCase(TestCase):

    def setup(self):
        user = User(name="TestUser", email="test@test.test")
        user.save()
        speech = Speech(user=user, name="Speech1")
        speech.save()

    def test_create(self):
        self.setup()
        audio_dir = "dummy/dir"
        speech = Speech.objects.get(name="Speech1")
        recording = Recording.create(speech=speech, audio_dir=audio_dir, transcript=[])
        self.assertNotEquals(recording, None)
        self.assertEquals(audio_dir, recording.audio_dir)
        self.assertEquals([], recording.transcript)

    def test_get_transcript_text(self):
        self.setup()
        audio_dir = "dummy/dir"
        speech = Speech.objects.get(name="Speech1")
        recording = Recording.create(speech=speech, audio_dir=audio_dir, transcript=[
            ("Hi I am a test", [], 0.92),
            ("Hi I am a test too", [], 0.95)
        ])
        transcript_text = recording.get_transcript_text()
        self.assertEquals(transcript_text.strip(), "Hi I am a test. Hi I am a test too.")

    def test_get_word_count(self):
        self.setup()
        audio_dir = "dummy/dir"
        speech = Speech.objects.get(name="Speech1")
        recording = Recording.create(speech=speech, audio_dir=audio_dir, transcript=[
            ("Hi I am test", [("Hi", 0, 1),("I", 1, 2),("am", 2, 3),("test", 3, 4)], 0.92),
            ("Hi I am test", [("Hi", 0, 1),("I", 1, 2),("am", 2, 3),("test", 3, 4)], 0.95)
        ])
        word_count = recording.get_word_count()
        self.assertEquals(word_count, 8)

    def test_get_recrding_length(self):
        self.setup()
        audio_dir = "dummy/dir"
        speech = Speech.objects.get(name="Speech1")
        recording = Recording.create(speech=speech, audio_dir=audio_dir, transcript=[
            ("Hi I am test", [("Hi", 0, 1),("I", 1, 2),("am", 2, 3),("test", 3, 4)], 0.92),
            ("Hi I am test", [("Hi", 5, 6),("I", 6, 7),("am", 7, 8),("test", 8, 9)], 0.95)
        ])
        audio_length = recording.get_recording_length()
        self.assertEquals(audio_length, 9)
