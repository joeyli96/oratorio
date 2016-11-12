from django.test import TestCase
from ..models import Recording, User, Speech


class RecordingTestCase(TestCase):
    def setup(self):
        user = User(name="TestUser", email="test@test.test")
        speech = Speech(user=user, name="Speech1")
        user.save()
        speech.save()

    def test_create(self):
        self.setup()
        print "Wow"
