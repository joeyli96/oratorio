# Django models for Coach
# Whether we have separate classes that mirror our class diagram is still up for
# debate

from __future__ import unicode_literals

import json
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
    """The Transcript class represents the transcript of a speech. It also records the start and end time for each word
        and the confidence for each sentence

        The transcript is stored as a list of tuples. Each tuple represents a sentence of the speech.
        The tuple is (transcript, wordTimestamps, confidence), where transcript is the transcript of the whole sentence,
        wordTimeStamps is a list with each element being a tuple (word, startTime, endTime)"""
    speech = models.ForeignKey(Speech, on_delete=models.CASCADE)
    audio_dir = models.CharField(max_length=255)
    audio_length = models.IntegerField(default=0)
    json_transcript = models.TextField()
    hesitations = models.IntegerField(default=0)
    neutrality = models.IntegerField(default=0)
    happiness = models.IntegerField(default=0)
    sadness = models.IntegerField(default=0)
    anger = models.IntegerField(default=0)
    fear = models.IntegerField(default=0)
    ml_score = models.IntegerField(default=0)
    transcript = []

    @staticmethod
    def create(speech, audio_dir, transcript):
        recording = Recording(speech=speech,
                  audio_dir=audio_dir,
                  json_transcript=json.dumps(transcript))
        recording.transcript = transcript
        recording.save()
        return recording

    def __str__(self):
        return "Recording " + str(self.id) + " from speech " + self.speech.name

    def get_transcript_text(self):
        """Returns the textual representation of the transcript (does not return the start and end time of each word)"""
        result = ""
        for sentence in self.transcript:
            result += sentence[0].strip() + ". "
        return result

    def get_word_count(self):
        """Returns the word count of the speech"""
        result = 0
        for sentence in self.transcript:
            result += len(sentence[1])
        return result

    def set_transcript(self, transcript):
        """This method creates and returns a transcript from the json object that is returned by IBM Watson's Speech To
        Text API"""
        self.transcript = transcript

