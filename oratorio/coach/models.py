# Django models for Coach
# Whether we have separate classes that mirror our class diagram is still up for
# debate

from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    def __str__(self):
        return "User " + self.name + ", email " + self.email

class Speech(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return "Speech " + self.name + " by user " + self.user.name

class Recording(models.Model):
    speech = models.ForeignKey(Speech, on_delete=models.CASCADE)
    audio_dir = models.CharField(max_length=255)
    audio_length = models.IntegerField()
    transcript = models.TextField()
    hesitations = models.IntegerField()
    neutrality = models.IntegerField()
    happiness = models.IntegerField()
    sadness = models.IntegerField()
    anger = models.IntegerField()
    fear = models.IntegerField()
    ml_score = models.IntegerField()

    def __str__(self):
        return "Recording " + self.id + " from speech " + self.speech.name
