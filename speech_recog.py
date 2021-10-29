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

def warning():
    tts = gTTS(text='I sincerely apologize for bad translation ahead, if someone is to be blamed its Google AI department. Enjoy', tld='ca', lang='en', slow=False)

    tts.save('sorry.mp3')

    playsound('E:\Code\speech100\sorry.mp3')
    
    return None


def speech_to_speech(number=0):
    start_time = time.time()

    fs = 44100 
    seconds = 30

    print("Recording...")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2, dtype='float64')
    sd.wait()
    print("Saving!")
    wavio.write('preaching{}.wav'.format(number), myrecording, fs ,sampwidth=2)

    print("Recording takes about: {} seconds".format(time.time() - start_time))

    r = sr.Recognizer()

    preaching = sr.AudioFile(
        'E:\Code\speech100\preaching{}.wav'.format(number))
    with preaching as source:
        audio = r.record(source)

    to_translate = r.recognize_google(audio, language="uk-UA")
    print(to_translate)

    translated = GoogleTranslator(
        source='ukrainian', target='english').translate(to_translate)
    print(translated)

    tts = gTTS(text=translated, tld='ca', lang='en', slow=True)

    tts.save('hello{}.mp3'.format(number))

    playsound('E:\Code\speech100\hello{}.mp3'.format(number))

    return None


def main():
    
    warning()
    
    n = 1
    while True and n <= 10:
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
