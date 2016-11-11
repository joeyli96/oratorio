from watson_developer_cloud import SpeechToTextV1
from settings import WATSON_USER_NAME, WATSON_PASSWORD
from models import Recording, Speech, User
import json


class Analyzer:
    @staticmethod
    def get_transcript_json(audio_dir):
        """This method calls the IBM Watson's speech API and returns the json that this produces"""
        speech_to_text = SpeechToTextV1(username=WATSON_USER_NAME, password=WATSON_PASSWORD)
        audio_file = open(audio_dir, "rb")
        # This is the call to IBM Watson's Speech to Text API
        # By default IBM Watson's Speech To Text API stops transcribing at the first long pause, setting continuous to
        # true overrides this behaviour. Setting time stamps to true gets the start and end time of each word
        json_transcript = speech_to_text.recognize(audio_file, content_type="audio/wav", continuous=True,
                                                   timestamps=True)
        return json_transcript['results']

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
    def create_recording(audio_dir, speech):
        """Given an audio file this method creates a transcript for this recording."""
        json_transcript = Analyzer.get_transcript_json(audio_dir)
        clean_transcript = Analyzer.clean_transcript(json_transcript)
        recording = Recording.create(speech=speech, audio_dir=audio_dir, transcript=clean_transcript)
        return recording
