# python test

import speech_recognition as sr

rec = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak")
    audio = rec.listen(source)


try:
    # can do with or without API key
    text = rec.recognize_google(audio)
    print("Quote: " + text)
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print("API error; ".format(e))

# experiments
# IBM - Watson text to speech