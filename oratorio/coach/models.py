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


class Transcript(models.Model):
    """The Transcript class represents the transcript of a speech. It also records the start and end time for each word
    and the confidence for each sentence

    The transcript is stored as a list of tuples. Each tuple represents a sentence of the speech.
    The tuple is (transcript, wordTimestamps, confidence), where transcript is the transcript of the whole sentence,
    wordTimeStamps is a list with each element being a tuple (word, startTime, endTime)"""

    def __init__(self, transcript):
        """Makes a transcript object and sets its transcript attribute to the parameter passed to it"""
        self.transcript = transcript

    def get_transcript(self):
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

    @staticmethod
    def clean_transcript(json_transcript):
        """Takes the json result returned by Watson and converts it into the format that the parameter requires (ie a
        list of sentences (as described above)). This method also removes any alternatives watson may return and only
        retains the alternative with the highest confidence."""
        transcript = []
        for sentence in json_transcript:
            # finalSentence is the sentence with the highest confidence
            # Watson is set up so that this is always the first alternative
            final_sentence = sentence["alternatives"][0]

            transcript.append((final_sentence["transcript"], final_sentence["timestamps"],
                               final_sentence["confidence"]))
        return transcript

    @staticmethod
    def create_transcript(json_transcript):
        """This method creates and returns a transcript from the json object that is returned by IBM Watson's Speech To
        Text API"""
        clean_transcript = Transcript.clean_transcript(json_transcript)
        transcript = Transcript(clean_transcript)
        return transcript
