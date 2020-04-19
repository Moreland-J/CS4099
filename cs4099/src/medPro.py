#!/usr/bin/env python

import sys
import os
import csv
import re
import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
from scipy.fftpack import fft

import pyaudio
import wave
import matplotlib.pyplot as plt

from slice import Slice
from comparisonTool import CompTool

from pydub import AudioSegment
from pydub.playback import play

running = True
selected = 1
db = []
categories = []
# selected acts as db index

# CONSTANT RUNNING INTERACTION
def run():
    readDB()

    while (running):
        userIn = input("Type the word you'd like to hear, 'filter' to filter results or 'exit' to leave the program.\n")
        if (userIn == "exit"):
            sys.exit()
        elif userIn == "filter":
            filter = None
            while filter == None:
                filter = input("AZ or ZA or section ordering? ")
            if filter == "AZ":
                displayDB(1, None)
            elif filter == "ZA":
                displayDB(2, None)
            else:
                displayDB(3, filter)

        elif (db.__contains__(userIn)):
            word = userIn

            # break into syllables
            # read from CSV and check if begins with or ends with
            toPrint = None
            fixWord = word
            with open('../database/fixes.csv') as file:
                reader = csv.reader(file, delimiter = ',')
                for col in reader:
                    fix = col[0]
                    if fix.endswith("-"):
                        fix = fix.replace("-", "")
                        # print(word + " " + fix)
                        if word.startswith(fix):
                            print(fix + " - ", end = "")
                            fixWord = re.sub(fix, "", word, 1)
                    else:
                        fix.replace("-", "")
                        if word.endswith(fix):
                            toPrint = fix
                            fixWord = re.sub(fix, "", word)
            slicer = Slice(fixWord, 3)
            slicer.slice()
            count = 0
            for morphs in slicer.morphemes:
                if count < len(slicer.morphemes) / 2 and count != len(slicer.morphemes) / 2 - 1:
                    print(morphs + " - ", end = "")
                elif count < len(slicer.morphemes) / 2:
                    print(morphs)
                count += 1
            if not toPrint == None:
                print(" - " + toPrint)

            # https://pythonbasics.org/python-play-sound/
            try:
                recording = playback(word, True)
                userIn = input("Would you like to attempt the word? Y/N or would you like a repeat? R ")
                while (userIn == 'r'):
                    recording = playback(word, True)
                    userIn = input("Would you like to attempt the word? Y/N or would you like a repeat? R ")
                if (userIn == 'y'):
                    # listen1(recording, word)
                    listen2(recording, word)
            except Exception as e:
                print(e)
                print("Audio recording does not exist for this word.")
        else:
            continue
    return


# READ DATABASE CSV FILE AND PRINT TO INTERFACE
def readDB():
    # https://realpython.com/python-csv/
    print()
    with open('../database/db.csv') as file:
        reader = csv.reader(file, delimiter = ',')
        count = 0
        for col in reader:
            if count == 0:
                count += 1
            else:
                db.append(col[0])
                categories.append(col[1].strip())
                print(db[count - 1])
                count += 1
    print()
    return

def displayDB(ordering, category):
    # 1 = A-Z, 2 = Z-A, 3 = section
    print()
    if ordering == 1:
        for word in db:
            print(word)
    elif ordering == 2:
        db.reverse()
        for word in db:
            print(word)
        db.reverse()
    elif ordering == 3:
        for i in range(len(db)):
            if categories[i] == category:
                print(db[i])

    print()
    return

# PLAY RECORDING FOR USER
def playback(word, listen):
    recording = AudioSegment.from_wav("../database/" + word + ".wav")
    if (listen):
        play(recording)
    return recording


def listen2(recording, word):
    # RECORD .WAV FILE
    fs = 16000
    d = 3   # no. of seconds for recording

    print("Speak")
    a = sd.rec(int(d * fs), fs, 1, blocking = 'True')
    # sd.play(a, fs)
    # plt.plot(a); plt.title("Speech")
    # plt.show()
    filename = "out.wav"
    # WRITE AS WAVE FILE
    sf.write(filename, a, fs)

    # COMPARISON
    tool = CompTool(filename, word)

    os.remove(filename)

# USE API TO LISTEN TO USER VOICE
# https://pythonprogramminglanguage.com/speech-recognition/
def listen1(recording, word):
    # GOOGLE API
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak")
        audio = rec.listen(source)
    try:
        print("Comparing")
        text = rec.recognize_google(audio)
        # IF YOU WANTED TO SHOW OTHER POSSIBLE HEARD WORDS SEE:
        # https://www.youtube.com/watch?v=b81-4qcWuTI TIMESTAMP: four:oh-six
        # REQUIRES PAYMENT PLUS NOT MISSING MEDICAL WORDS
        compare(word, text)
        return
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("API error; ".format(e))            


# COMPARE DB WORD TO USER ATTEMPT
def compare(word, userWord):
    if (word == userWord):
        print("Correct!")
    else:
        print("Not quite.")
    return

run()