from numpy import number
import speech_recognition as sr
import sounddevice as sd
from scipy.io.wavfile import write
from deep_translator import GoogleTranslator
import time
from gtts import gTTS
import wavio
from playsound import playsound
from threading import Thread

PATH = 'E:\Code\speech100'

stt_lang = "uk-UA"
tts_lang = 'en'
from_lang = 'ukrainian'
to_lang = 'english'
accent = 'ca'


def warning():
    tts = gTTS(text='I sincerely apologize for bad translation ahead, if someone is to be blamed its Google AI department. Enjoy',
               tld=accent, lang=tts_lang, slow=False)

    tts.save('sorry.mp3')

    playsound('{}\sorry.mp3'.format(PATH))

    return None


def speech_to_speech(number=0):
    start_time = time.time()

    fs = 44100
    seconds = 30

    print("Recording...")

    myrecording = sd.rec(int(seconds * fs), samplerate=fs,
                         channels=2, dtype='float64')
    sd.wait()

    print("Saving!")
    wavio.write('preaching{}.wav'.format(number), myrecording, fs, sampwidth=2)

    print("Recording takes about: {} seconds".format(time.time() - start_time))

    r = sr.Recognizer()

    preaching = sr.AudioFile(
        '{}\preaching{}.wav'.format(PATH, number))
    with preaching as source:
        audio = r.record(source)

    to_translate = r.recognize_google(audio, language=stt_lang)
    print(to_translate)

    translated = GoogleTranslator(
        source=from_lang, target=to_lang).translate(to_translate)
    print(translated)

    tts = gTTS(text=translated, tld=accent, lang=tts_lang, slow=True)

    tts.save('hello{}.mp3'.format(number))

    playsound('{}\hello{}.mp3'.format(PATH, number))

    return None


def main():

    warning()

    n = 1
    while True and n <= 180:
        start_time = time.time()

        t1 = Thread(target=speech_to_speech, args=(n,))
        t2 = Thread(target=speech_to_speech, args=(n+1,))

        t1.start()
        time.sleep(30.2)

        t2.start()
        time.sleep(30.2)

        t1.join()
        t2.join()

        n += 2
        print("Loop takes about: {} seconds".format(time.time() - start_time))


if __name__ == "__main__":
    main()
