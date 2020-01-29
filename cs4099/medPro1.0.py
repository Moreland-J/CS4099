#!/usr/bin/env python

import sys
import csv
import speech_recognition as sr

from slice import Slice

from pydub import AudioSegment
from pydub.playback import play

running = True
selected = 1
word = "null"
db = []
# selected acts as db index

def readDB():
    # https://realpython.com/python-csv/
    with open('database/db.csv') as file:
        reader = csv.reader(file, delimiter = ',')
        count = 0
        for col in reader:
            if count == 0:
                count += 1
            else:
                db.append(col[0])
                print(db[count - 1])
                count += 1
    print()
    return

# CONSTANT RUNNING INTERACTION
def run():
    global word
    while (running):
        userIn = input("Type the word you'd like to hear or 'exit' to leave the program.\n")
        if (userIn == "exit"):
            sys.exit()
        elif (db.__contains__(userIn)):
            word = userIn

            # break into syllables
            slicer = Slice(word, 8)
            slicer.slice()
            for morphs in slicer.morphemes:
                print(morphs)

            # https://pythonbasics.org/python-play-sound/
            song = AudioSegment.from_wav("database/" + userIn + ".wav")
            play(song)
            userIn = input("Would you like to attempt the word? Y/N ")
            if (userIn == 'y'):
                listen()
        else:
            continue
    return

# USE API TO LISTEN TO USER VOICE
# https://pythonprogramminglanguage.com/speech-recognition/
def listen():
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak")
        audio = rec.listen(source)
    try:
        print("Comparing")
        text = rec.recognize_google(audio)
        compare(text)
        return
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("API error; ".format(e))            

# COMPARE DB WORD TO USER ATTEMPT
def compare(userWord):
    if (word == userWord):
        print("Correct!")
    else:
        print("Not quite.")
    return

readDB()
run()