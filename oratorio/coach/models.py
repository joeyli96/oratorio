# Django models for Coach
# This class contains the models used to hold data and as a schema
# for the django database.

from __future__ import unicode_literals

import json
from django.db import models
from analyzer import Analyzer


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)

    def __str__(self):
       return "User " + self.name + ", email " + self.email

    def get_avg_pace(self):
        "Return the average pace of all the speeches this user owns"
        res = 0.0
        speeches = Speech.objects.filter(user=self)
        if speeches:
            for speech in speeches:
                res += speech.get_avg_pace()
            res = round(res / len(speeches), 2)
        return res
    
    def get_avg_tone(self):
        "Return a dict where keys are types of emotions and values are the \
        average values of those emotions for the user"
        speeches = Speech.objects.filter(user=self)
        res = { 'joy': 0.0, 'sadness': 0.0, 'anger': 0.0,
                'fear': 0.0, 'disgust': 0.0, 'confident': 0.0 }
        if speeches:
            for speech in speeches:
                avg_tone = speech.get_avg_tone()
                res['joy'] += avg_tone['joy']
                res['sadness'] += avg_tone['sadness']
                res['anger'] += avg_tone['anger']
                res['fear'] += avg_tone['fear']
                res['disgust'] += avg_tone['disgust']
                res['confident'] += avg_tone['confident']
            res['joy'] = round(res['joy'] / len(speeches), 2)
            res['sadness'] = round(res['sadness'] / len(speeches), 2)
            res['anger'] = round(res['anger'] / len(speeches), 2)
            res['fear'] = round(res['fear'] / len(speeches), 2)
            res['disgust'] = round(res['disgust'] / len(speeches), 2)
            res['confident'] = round(res['confident'] / len(speeches), 2)
        return res

    def get_avg_pauses(self):
        speeches = Speech.objects.filter(user=self)
        res = 0.0
        if speeches:
            for speech in speeches:
                res += speech.get_avg_pauses()
            res = round(res / len(speeches), 2)
        return res

class Speech(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return "Speech " + self.name + " by user " + self.user.name

    def get_avg_pace(self):
        "Return the average pace of all the recordings in this speech"
        res = 0.0
        recs = Recording.objects.filter(speech=self)
        if recs:
            for rec in recs:
                res += rec.get_avg_pace()
            res = round(res / len(recs), 2)
        return res

    def get_avg_tone(self):
        "Return a dict where keys are types of emotions and values are the \
        average values of those emotions for the speech"
        recs = Recording.objects.filter(speech=self)
        res = { 'joy': 0.0, 'sadness': 0.0, 'anger': 0.0,
                'fear': 0.0, 'disgust': 0.0, 'confident': 0.0 }
        if recs:
            for rec in recs:
                res['joy'] += rec.joy
                res['sadness'] += rec.sadness
                res['anger'] += rec.anger
                res['fear'] += rec.fear
                res['disgust'] += rec.disgust
                res['confident'] += rec.confident
            res['joy'] = round(res['joy'] / len(recs), 2)
            res['sadness'] = round(res['sadness'] / len(recs), 2)
            res['anger'] = round(res['anger'] / len(recs), 2)
            res['fear'] = round(res['fear'] / len(recs), 2)
            res['disgust'] = round(res['disgust'] / len(recs), 2)
            res['confident'] = round(res['confident'] / len(recs), 2)
        return res

    def get_avg_pauses(self):
        recs = Recording.objects.filter(speech=self)
        res = 0.0
        if recs:
            for rec in recs:
                res += rec.pauses
            res = round(res / len(recs), 2)
        return res
        

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
    json_tone_analysis = models.TextField()
    pauses = models.IntegerField(default=0)
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
            json_tone_analysis = Analyzer.get_tone_analysis_json(audio_dir)
            tone_analysis = Analyzer.clean_tone_analysis(json_tone_analysis, transcript)
        recording = Recording(speech=speech,
                  audio_dir=audio_dir,
                  json_transcript=json.dumps(transcript))
        if tone_analysis:
            recording.json_tone_analysis = json.dumps(tone_analysis)
        transcript_text = recording.get_transcript_text()
        if transcript_text:
            tone_dictionary = Analyzer.get_emotion(transcript_text)
            recording.disgust = tone_dictionary["disgust"]
            recording.joy = tone_dictionary["joy"]
            recording.sadness = tone_dictionary["sadness"]
            recording.anger = tone_dictionary["anger"]
            recording.fear = tone_dictionary["fear"]
            recording.confident = tone_dictionary["confident"]
        pause_list, recording.pauses = Analyzer.get_pauses(transcript)
        recording.save()
        return recording

    def get_analysis(self):
        if not self.json_tone_analysis:
            return {}
        return json.loads(self.json_tone_analysis)

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
