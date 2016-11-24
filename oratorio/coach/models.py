# Django models for Coach
# This class contains the models used to hold data and as a schema
# for the django database.
#
# TODO: Separate classes that mirror class diagram?

from __future__ import unicode_literals

import json
from django.db import models
from analyzer import Analyzer


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)

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
    disgust = models.IntegerField(default=0)
    joy = models.IntegerField(default=0)
    sadness = models.IntegerField(default=0)
    anger = models.IntegerField(default=0)
    fear = models.IntegerField(default=0)
    confident = models.IntegerField(default=0)
    ml_score = models.IntegerField(default=0)

    @staticmethod
    def create(speech, audio_dir, transcript=None):
        # Optional transcript used for testing
        if transcript is None and audio_dir != "dummy/dir":
            json_transcript = Analyzer.get_transcript_json(audio_dir)
            transcript = Analyzer.clean_transcript(json_transcript)
        recording = Recording(speech=speech,
                  audio_dir=audio_dir,
                  json_transcript=json.dumps(transcript))
        transcript_text = recording.get_transcript_text()
        if transcript_text:
            tone_dictionary = Analyzer.get_emotion(transcript_text)
            recording.disgust = tone_dictionary["disgust"]
            recording.joy = tone_dictionary["joy"]
            recording.sadness = tone_dictionary["sadness"]
            recording.anger = tone_dictionary["anger"]
            recording.fear = tone_dictionary["fear"]
            recording.confident = tone_dictionary["confident"]

        recording.save()
        return recording

    def __str__(self):
        return "Recording " + str(self.id) + " from speech " + self.speech.name

    def get_transcript_text(self):
        """Returns the textual representation of the transcript (does not return the start and end time of each word)"""
        transcript = self.get_transcript()
        result = ""
        for sentence in transcript:
            result += sentence[0].strip() + ". "
        return result

    def get_word_count(self):
        """Returns the word count of the speech"""
        transcript = self.get_transcript()
        result = 0
        for sentence in transcript:
            result += len(sentence[1])
        return result

    def get_recording_length(self):
        """Returns the length of the recording in seconds"""
        transcript = self.get_transcript()
        if not transcript:
            return 0
        last_sentence = transcript[-1]
        last_sentence_words = last_sentence[1]
        last_word = last_sentence_words[-1]
        last_word_end_timestamps = last_word[2]

        first_sentence = transcript[0]
        first_sentence_words = first_sentence[1]
        first_word = first_sentence_words[0]
        first_sentence_start_timestamp = first_word[1]

        return last_word_end_timestamps - first_sentence_start_timestamp
    
    def get_avg_pace(self):
        rec_len = self.get_recording_length()
        if rec_len != 0:
            res = 60 * self.get_word_count() / rec_len
        else:
            res = 0
        return round(res, 2)

    def get_tone(self):
        tones = {
            'joy': self.joy,
            'sadness': self.sadness,
            'anger': self.anger,
            'fear': self.fear,
        }
        maxVal = float('-inf')
        res = None
        for key, value in tones.iteritems():
            if value > maxVal:
                maxVal = value
                res = key
        return res
    
    def get_transcript(self):
        return json.loads(self.json_transcript)
