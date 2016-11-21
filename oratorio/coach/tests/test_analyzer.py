from ..models import Speech, Recording, User
from ..analyzer import Analyzer
from django.test import TestCase

class AnalyzerTestCase(TestCase):
    def setup(self):
        user = User(name="TestUser", email="test@test.test")
        user.save()
        speech = Speech(user=user, name="Speech1")
        speech.save()

    def test_get_5_most_frequent_words(self):
        # tests that only the 5 most frequent words are returned
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
        # tests that if the transcript contains less than 5 words then only these are added
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
        self.setup()
        speech = Speech.objects.get(name="Speech1")
        recording = Recording.create(speech, "dummy/dir", transcript=[
            (
            "I am his her", [("I", 0, 1), ("am", 1, 2), ("his", 2, 3), ("her", 3, 4)], 0.92),
        ])
        frequent_words = Analyzer.get_word_frequency(recording.get_transcript_text(), 5)
        self.assertEquals(frequent_words, [])