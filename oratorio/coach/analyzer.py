from watson_developer_cloud import SpeechToTextV1
from settings import WATSON_USER_NAME, WATSON_PASSWORD, COACH_ROOT
from models import Recording, Speech, User
from collections import Counter
import re

# A pause is considered a pause if it is longer than (THREDSHOLD)s
THRESHOLD = 1.5

# STOP_WORDS will not be counted in the word frequency
STOP_WORDS = ["a", "am", "an", "and", "any", "are", "as", "at", "be", \
              "because", "been", "but", "by", "can", "cannot", "could", \
              "did", "do", "does", "every", "for", "from", "get", "got", \
              "had", "has", "have", "he", "her", "hers", "him", "his", \
              "how", "i", "in", "into", "is", "it", "its", "may", "me", \
              "might", "most", "must", "my", "neither", "no", "nor", "not", \
              "of", "off", "on", "or", "other", "our", "own", "she", \
              "should", "so", "some", "than", "that", "the", "their", \
              "them", "then", "there", "they", "this", "tis", "to", "too", \
              "twas", "us", "was", "we", "were", "what", "when", "where", \
              "which", "while", "who", "whom", "why", "will", "with", "would", \
              "you", "your"]

class Analyzer:
    """This class creates recordings and performs the analysis on a recording. It calls Watson's speech to text API to
    get the transcript and BeyondVerbal to get the tone of the speech, counts the frequently used words and pauses"""

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

    @staticmethod
    def get_word_frequency(transcript_text, k):
        """Given transcript, returns k of the most frequently used words in transcript. (ignores STOP WORDS)"""
        if not transcript_text:
            return []
        word_frequencies = Counter()
        transcript_text = re.sub("[.]", "", transcript_text.lower().strip())
        for word in re.split("\s+", transcript_text):
            if word not in STOP_WORDS:
                word_frequencies[word] += 1
        return word_frequencies.most_common(k)

    # @staticmethod
    # def get_emotions(audio_dir):


    @staticmethod
    def get_pauses(transcript):
        """Given transcript (with stop an end times, see Recording in models.py for format), returns the number of pauses
        and where they occur. Eg: If get_pauses(a_transcript) returns ([1, 0, 1, 1, 0], 3) This means that the speech
        has 3 pauses one after the 1st, 3rd and 4th word, there was no pause after words 2 and 5 (and there are 6 words)
        A pause is only counted as a pause if it is longer than the THRESHOLD"""
        start_end_times = []
        pauses = 0

        for list in [item[1] for item in transcript]:
            for item in list:
                start_end_times.append(item[1:]) # we only want start and end times

        pause_list = [0]*(len(start_end_times)-len(transcript))  # stores an array with where pauses are

        for i in range(0, len(start_end_times)-1):
            if start_end_times[i+1][0] - start_end_times[i][1] >= THRESHOLD:
                pause_list[i] = 1
                pauses += 1

        return (pause_list, pauses)
