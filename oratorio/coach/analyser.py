from watson_developer_cloud import SpeechToTextV1
from models import Transcript
from secret_settings import WATSON_USER_NAME, WATSON_PASSWORD


class Analyzer:
    @staticmethod
    def get_transcript_json(audio_file_name):
        """This method calls the IBM Watson's speech API and returns the json that this produces"""
        speech_to_text = SpeechToTextV1(username=WATSON_USER_NAME, password=WATSON_PASSWORD)
        audio_file = open(audio_file_name, "rb")
        # This is the call to IBM Watson's Speech to Text API
        # By default IBM Watson's Speech To Text API stops transcribing at the first long pause, setting continuous to
        # true overrides this behaviour. Setting time stamps to true gets the start and end time of each word
        json_transcript = speech_to_text.recognize(audio_file, content_type="audio/wav", continuous=True,
                                                   timestamps=True)
        return json_transcript['results']

    @staticmethod
    def create_transcript(audio_file_name):
        """Given an audio file this method creates a transcript for this recording."""
        json_transcript = Analyzer.get_transcript_json(audio_file_name)
        transcript = Transcript.createTranscript(json_transcript)
        return transcript
