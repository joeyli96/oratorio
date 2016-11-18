from django.test import TestCase
from ..models import Recording, User, Speech
from ..analyzer import Analyzer

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

    def test_get_recording_length(self):
        self.setup()
        audio_dir = "dummy/dir"
        speech = Speech.objects.get(name="Speech1")
        recording = Recording.create(speech=speech, audio_dir=audio_dir, transcript=[
            ("Hi I am test", [("Hi", 0, 1),("I", 1, 2),("am", 2, 3),("test", 3, 4)], 0.92),
            ("Hi I am test", [("Hi", 5, 6),("I", 6, 7),("am", 7, 8),("test", 8, 9)], 0.95)
        ])
        audio_length = recording.get_recording_length()
        self.assertEquals(audio_length, 9)

    def test_empty_recording(self):
        self.setup()
        speech = Speech.objects.get(name="Speech1")
        recording = Recording.create(speech, "dummy/dir", [])
        self.assertEquals(recording.get_word_count(), 0)
        self.assertEquals(recording.get_transcript_text(), "")

    # Tests for unimplement functionality
    # These tests check that the most frequent words can be retrieved from the recording

    def test_get_5_most_frequent_words(self):
        # tests that only the 5 most frequent words are returned
        self.setup()
        speech = Speech.objects.get(name="Speech1")
        recording = Recording.create(speech, "dummy/dir", transcript=[
            ("Hi a Hi I Hi", [("Hi", 0, 1), ("a", 1, 2), ("Hi", 2, 3), ("I", 3, 4), ("Hi", 4, 5)], 0.92),
            ("I I I Hi", [("I", 5, 6), ("I", 6, 7), ("I", 7, 8), ("Hi", 8, 9)], 0.95),
            ("am am test", [("am", 9, 10), ("am", 10, 11), ("test", 12, 13)], 0.95),
            ("a Hi", [("a", 13, 14), ("Hi", 15, 16), ], 0.95),
            ("am test", [("am", 13, 14), ("test", 14, 15)], 0.95),
            ("xxx", [("xxx", 15, 16)], 0.95)
        ])
        frequent_words = Analyzer.get_word_frequency(recording.get_transcript_text(), 5)
        self.assertEquals(len(frequent_words), 5)
        self.assertEquals(frequent_words[0], ("hi", 5))
        self.assertEquals(frequent_words[1], ("i", 4))
        self.assertEquals(frequent_words[2], ("am", 3))
        self.assertEquals(frequent_words[3], ("a", 2))
        self.assertEquals(frequent_words[4], ("test", 2))
        self.assertNotIn("xxx", frequent_words.keys())

    def test_get_most_frequent_words_less_than_5(self):
        # tests that if the transcript contains less than 5 words then only these are added
        self.setup()
        speech = Speech.objects.get(name="Speech1")
        recording = Recording.create(speech, "dummy/dir", transcript=[
            ("Hi a Hi I Hi", [("Hi", 0, 1), ("a", 1, 2), ("Hi", 2, 3), ("I", 3, 4), ("Hi", 4, 5)], 0.92),
        ])
        frequent_words = Analyzer.get_word_frequency(recording.get_transcript_text(), 5)
        self.assertEquals(len(frequent_words), 3)
        self.assertEquals(frequent_words[0], ("hi", 3))
        self.assertEquals(frequent_words[1], ("i", 1))
        self.assertEquals(frequent_words[2], ("a", 1))
