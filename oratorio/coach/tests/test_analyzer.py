from ..models import Speech, Recording, User
from ..analyzer import Analyzer
from django.test import TestCase
import json

class AnalyzerTestCase(TestCase):
    """Tests for the Analyzer class in analyzer.py"""

    def setup(self):
        """Sets up the database for the analyzer"""
        user = User(name="TestUser", email="test@test.test")
        user.save()
        speech = Speech(user=user, name="Speech1")
        speech.save()

    # The following tests test the analysis of the most frequently used words

    def test_get_5_most_frequent_words(self):
        """tests that only the 5 most frequent words are returned"""
        self.setup()
        speech = Speech.objects.get(name="Speech1")
        recording = Recording.create(speech, "dummy/dir", transcript=[
            ("Hiss ab Hiss Ix Hiss", [("Hiss", 0, 1), ("ab", 1, 2), ("Hiss", 2, 3), ("Ix", 3, 4), ("Hiss", 4, 5)], 0.92),
            ("Ix Ix Ix Hiss", [("Ix", 5, 6), ("Ix", 6, 7), ("Ix", 7, 8), ("Hiss", 8, 9)], 0.95),
            ("mam mam test", [("mam", 9, 10), ("mam", 10, 11), ("test", 12, 13)], 0.95),
            ("ab Hiss", [("ab", 13, 14), ("Hiss", 15, 16), ], 0.95),
            ("mam test", [("mam", 13, 14), ("test", 14, 15)], 0.95),
            ("xxx", [("xxx", 15, 16)], 0.95)
        ])
        frequent_words = Analyzer.get_word_frequency(recording.get_transcript_text(), 5)
        self.assertEquals(len(frequent_words), 5)
        self.assertEquals(frequent_words[0], ("hiss", 5))
        self.assertEquals(frequent_words[1], ("ix", 4))
        self.assertEquals(frequent_words[2], ("mam", 3))
        self.assertEquals(frequent_words[3], ("ab", 2))
        self.assertEquals(frequent_words[4], ("test", 2))
        self.assertNotIn("xxx", [item[0] for item in frequent_words])

    def test_get_most_frequent_words_less_than_5(self):
        """tests that if the transcript contains less than 5 words then only these are added"""
        self.setup()
        speech = Speech.objects.get(name="Speech1")
        recording = Recording.create(speech, "dummy/dir", transcript=[
            ("Hiss ab Hiss Ix Hiss", [("Hiss", 0, 1), ("ab", 1, 2), ("Hiss", 2, 3), ("Ix", 3, 4), ("Hiss", 4, 5)], 0.92),
        ])
        frequent_words = Analyzer.get_word_frequency(recording.get_transcript_text(), 5)
        self.assertEquals(len(frequent_words), 3)
        self.assertEquals(frequent_words[0], ("hiss", 3))
        self.assertEquals(frequent_words[1], ("ix", 1))
        self.assertEquals(frequent_words[2], ("ab", 1))

    def test_stop_words(self):
        """tests that the stop words are not counted and do not effect the counting of other words"""
        self.setup()
        speech = Speech.objects.get(name="Speech1")
        recording = Recording.create(speech, "dummy/dir", transcript=[
            ("I am his her", [("I", 0, 1), ("am", 1, 2), ("his", 2, 3), ("her", 3, 4)], 0.92),
        ])
        frequent_words = Analyzer.get_word_frequency(recording.get_transcript_text(), 5)
        self.assertEquals(frequent_words, [])
        recording = Recording.create(speech, "dummy/dir", transcript=[
            ("I am his xyz", [("I", 0, 1), ("am", 1, 2), ("his", 2, 3), ("xyz", 3, 4)], 0.92),
        ])
        frequent_words = Analyzer.get_word_frequency(recording.get_transcript_text(), 5)
        self.assertEquals(len(frequent_words), 1)
        self.assertEquals(frequent_words[0], ("xyz", 1))

    # The following tests, test the analysis of pauses in a speech.
    # The threshold for a pause in our system is 1.5 (ie if a pause >= 1.5s it is counted as a pause)

    def test_no_pauses(self):
        """tests a speech which has a pause that is just under the threshold"""
        self.setup()
        speech = Speech.objects.get(name="Speech1")
        recording = Recording.create(speech, "dummy/dir", transcript=[
            ("I am his her", [("I", 0, 1), ("am", 1, 2), ("his", 2, 3), ("her", 4.49999999, 4)], 0.92),
        ])
        pauses = Analyzer.get_pauses(recording.get_transcript())
        self.assertEquals(pauses[1], 0)
        self.assertEquals(pauses[0], [0] * 3)

    def test_pause(self):
        """tests a speech which has a pause that is just at the threshold"""
        self.setup()
        speech = Speech.objects.get(name="Speech1")
        recording = Recording.create(speech, "dummy/dir", transcript=[
            ("I am his her", [("I", 0, 1), ("am", 1, 2), ("his", 2, 3), ("her", 4.5, 5)], 0.92),
        ])
        pauses = Analyzer.get_pauses(recording.get_transcript())
        self.assertEquals(pauses[1], 1)
        self.assertEquals(pauses[0], [0, 0, 1])

    def test_bounds(self):
        """tests that pauses are counted correctly at the beginning and ends of speeches"""
        self.setup()
        speech = Speech.objects.get(name="Speech1")
        # with pauses at beginning and end
        recording = Recording.create(speech, "dummy/dir", transcript=[
            ("I am his her", [("I", 0, 1), ("am", 2.5, 3), ("his", 3, 4), ("her", 5.5, 6)], 0.92),
        ])
        pauses = Analyzer.get_pauses(recording.get_transcript())
        self.assertEquals(pauses[1], 2)
        self.assertEquals(pauses[0], [1, 0, 1])
        # without pauses at beginning and end
        recording = Recording.create(speech, "dummy/dir", transcript=[
            ("I am his her", [("I", 0, 1), ("am", 2.49999999, 3), ("his", 3, 4), ("her", 5.49999999, 6)], 0.92),
        ])
        pauses = Analyzer.get_pauses(recording.get_transcript())
        self.assertEquals(pauses[1], 0)
        self.assertEquals(pauses[0], [0] * 3)

    def test_multisentence_speech(self):
        """checks that pauses are counted correctly across multiple sentences (even when a pause occurs across a sentence)"""
        self.setup()
        speech = Speech.objects.get(name="Speech1")
        recording = Recording.create(speech, "dummy/dir", transcript=[
            ("I am his her", [("I", 0, 1), ("am", 2.5, 3), ("his", 4.5, 4), ("her", 5.5, 6)], 0.92),
            ("I am a sentence2", [("I", 7.5, 8), ("am", 9, 10), ("a", 11.5, 12), ("sentence2", 5.5, 6)], 0.12),
        ])
        pauses = Analyzer.get_pauses(recording.get_transcript())
        self.assertEquals(pauses[1], 5)
        self.assertEquals(pauses[0], [1, 1, 1, 1, 0, 1])
        recording = Recording.create(speech, "dummy/dir", transcript=[
            ("I am his her", [("I", 0, 1), ("am", 2.5, 3), ("his", 4.5, 4), ("her", 5.5, 6)], 0.92),
            ("I am a sentence2", [("I", 7.4999999, 8), ("am", 9, 10), ("a", 11.5, 12), ("sentence2", 5.5, 6)], 0.12),
        ])
        pauses = Analyzer.get_pauses(recording.get_transcript())
        self.assertEquals(pauses[1], 4)
        self.assertEquals(pauses[0], [1, 1, 1, 0, 0, 1])

    def test_emotion_analyzer_joy(self):
        self.setup()
        speech = Speech.objects.get(name="Speech1")
        recording = Recording.create(speech, "dummy/dir", transcript=[
            ("I am very happy", [("I", 0, 1), ("am", 2.5, 3), ("his", 4.5, 4), ("her", 5.5, 6)], 0.92),
            ("I am very very very joyful", [("I", 7.5, 8), ("am", 9, 10), ("a", 11.5, 12), ("sentence2", 5.5, 6)], 0.12),
        ])
        tone_dictionary = Analyzer.get_emotion(recording.get_transcript_text())

        # assert that the sentence is sufficiently joyful :)
        self.assertGreater(tone_dictionary["joy"], 80)
        self.assertLess(tone_dictionary["sadness"], 20)

