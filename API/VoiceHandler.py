import speech_recognition as sr
from pydub import AudioSegment
import subprocess
import os
from gtts import gTTS


def get_audio_file(text):
    tts = gTTS(text=text, lang='en')
    tts.save("file.mp3")


def CheckExtension(audioFile):
    parts = audioFile.split('.')
    extension = parts[-1]
    parts[-1] = "wav"
    if not(extension=='wav'):
        original = AudioSegment.from_file(os.getcwd()+'/'+audioFile, format=extension)
        original.export(os.getcwd()+'/' + ".".join(parts), format="wav")
        return ".".join(parts)
    return audioFile


def ExtractText(audioFile):

    words = audioFile.split('.')
    words[-1] = 'wav'
    dest_filename = ".".join(words)
    process = subprocess.run(['ffmpeg', '-i', audioFile, dest_filename])
    subprocess.run(['rm',audioFile])
    audioFile = dest_filename

    try:
        recognizer = recognizer = sr.Recognizer()
        speech = sr.AudioFile(audioFile)
        with speech as source:
            audio = recognizer.record(source)
            extractedText = recognizer.recognize_google(audio)
            extractedText = extractedText.lower()
    except sr.RequestError as e: 
        extractedText = "Could not request results; {0}".format(e)
    
    except sr.UnknownValueError: 
        extractedText="unknown error occured"
    
    subprocess.run(['rm',audioFile])
    return extractedText

# Check the feature by uncommenting the following line
# print(ExtractText("API/audios/VoiceSample.m4a"))
