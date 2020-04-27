#!/usr/bin/env python
import tkinter
import scipy
import pydub
from tkinter import *

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
                    listen1(recording, word)
                    # listen2(recording, word)
            except Exception as e:
                print(e)
                print("Audio recording does not exist for this word.")
        else:
            continue
    return

def uiRun(userIn):
    if (db.__contains__(userIn)):
            word = userIn

            # break into syllables
            # read from CSV and check if begins with or ends with
            toPrint = None
            fixWord = word
            with open('../database/fixes.csv') as file:
                reader = csv.reader(file, delimiter = ',')
                split = ""
                for col in reader:
                    fix = col[0]
                    # PREFIX
                    if fix.endswith("-"):
                        fix = fix.replace("-", "")
                        # print(word + " " + fix)
                        if word.startswith(fix):
                            split = fix + " - "
                            print(fix + " - ", end = "")
                            fixWord = re.sub(fix, "", word, 1)
                    # SUFFIX
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
                    split = split + morphs + " - "
                    print(morphs + " - ", end = "")
                elif count < len(slicer.morphemes) / 2:
                    split = split + morphs
                    print(morphs)
                count += 1
            # SUFFIX ADDITION
            if not toPrint == None:
                split = split + " - " + toPrint
                print(" - " + toPrint)
            
            popup = Tk()
            popup.geometry("300x300")
            popup.title("Syllables")
            frame5 = Frame(popup)
            frame5.pack()
            label = Label(frame5, text = split)
            label.pack(pady = 10)
            # scroll = Scrollbar(popup)
            # scroll.pack(side = RIGHT, fill = Y)
            # scroll.config(command = popup.yview)

            try:
                frame6 = Frame(popup)
                frame6.pack()
                
                replay = Button(frame6, text = "Replay", command = lambda: playback(word, True))
                replay.pack(side = "left", padx = 5, pady = 10)
                attempt = Button(frame6, text = "Attempt", command = lambda: listen(recording, word, popup, frame7))
                attempt.pack(side = "left", padx = 5, pady = 10)
                cancel = Button(frame6, text = "Cancel", command = lambda: close(popup))
                cancel.pack(side = "left", padx = 5, pady = 10)
                frame7 = Frame(popup)
                frame7.pack()
                recording = playback(word, True)

            except Exception as e:
                print(e)
                print("Audio recording does not exist for this word.")
                if not "Audio recording does not exist for this word." in split:
                    split = split + " - " + "Audio recording does not exist for this word."

def listen(recording, word, popup, frame7):
    global ch
    if ch.get() == 0:
        listen1(recording, word, popup, frame7)
    else:
        listen2(recording, word, popup, frame7)

def close(root):
    root.destroy()


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
                terms.insert(count, col[0])
    print()
    scroll = Scrollbar(frame, orient = "vertical")
    scroll.config(command = terms.yview)
    scroll.pack(side = "right", fill = "y")
    terms.config(yscrollcommand = scroll.set)
    root.mainloop()
    return

def displayDB(ordering, category):
    # 1 = A-Z, 2 = Z-A, 3 = section
    terms.delete(0, terms.size())
    if category == "all":
        ordering = 1
    print()
    count = 1
    if ordering == 1:
        for word in db:
            print(word)
            terms.insert(count, word)
            count += 1
    elif ordering == 2:
        db.reverse()
        for word in db:
            print(word)
            terms.insert(count, word)
            count += 1
        db.reverse()
    elif ordering == 3:
        for i in range(len(db)):
            if categories[i] == category:
                print(db[i])
                terms.insert(count, db[i])
                count += 1

    print()
    return

# PLAY RECORDING FOR USER
def playback(word, listen):
    global speedbox
    speed = 1.0
    if not speedbox.get() == "":
        try:
            speed = float(speedbox.get())
        except:
            print("not a float")
            speed = 1.0
    recording = AudioSegment.from_file("../database/" + word + ".wav", "wav")
    if (listen):
        sound_with_altered_frame_rate = recording
        if speed < 1.51 and speed > 0.39:
            print(speed)
            sound_with_altered_frame_rate = recording._spawn(recording.raw_data, overrides = {
                "frame_rate": int(recording.frame_rate * speed)
            })
            sound_with_altered_frame_rate.set_frame_rate(recording.frame_rate)
        play(sound_with_altered_frame_rate)
    return recording

def playbackUser(currAttempt):
    global speedbox
    speed = 1.0
    if not speedbox.get() == "":
        try:
            speed = float(speedbox.get())
        except:
            print("not a float")
            speed = 1.0
    recording = AudioSegment.from_file("out" + str(currAttempt) + ".wav", "wav")
    adapted = recording
    if speed < 1.51 and speed > 0.39:
        print(speed)
        adapted = recording._spawn(recording.raw_data, overrides = {
            "frame_rate": int(recording.frame_rate * speed)
        })
        adapted.set_frame_rate(recording.frame_rate)
    play(adapted)
    return recording

# USE API TO LISTEN TO USER VOICE
# https://pythonprogramminglanguage.com/speech-recognition/
def listen1(recording, word, result, frame):
    # GOOGLE API
    frame.destroy()
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak 1")
        audio = rec.listen(source)
    try:
        print("Comparing")
        text = rec.recognize_google(audio)
        # IF YOU WANTED TO SHOW OTHER POSSIBLE HEARD WORDS SEE:
        # https://www.youtube.com/watch?v=b81-4qcWuTI TIMESTAMP: four:oh-six
        # REQUIRES PAYMENT PLUS NOT MISSING MEDICAL WORDS
        compare(word, text, result)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("API error; ".format(e))            

attempt = 0
def listen2(recording, word, result, frame):
    global attempt
    attempt += 1
    frame7 = Frame(result)
    frame7.pack()
    response = Button(frame7, text = attempt, command = lambda: playbackUser(response['text']))
    response.pack(pady = 10)

    # RECORD .WAV FILE
    fs = 16000
    d = 3   # no. of seconds for recording

    print("Speak 2")
    a = sd.rec(int(d * fs), fs, 1, blocking = 'True')
    # sd.play(a, fs)
    # plt.plot(a); plt.title("Speech")
    # plt.show()
    filename = "out" + str(attempt) + ".wav"
    # WRITE AS WAVE FILE
    sf.write(filename, a, fs)

    # COMPARISON
    tool = CompTool(filename, word)

    # os.remove(filename)


# COMPARE DB WORD TO USER ATTEMPT
def compare(word, userWord, popup):
    frame7 = Frame(popup)
    frame7.pack()
    response = Label(frame7, text = "")
    response.pack(pady = 10)
    # wav = attempt - 1
    # playback = Button(frame7, text = "Repeat", command = lambda: playbackUser(wav))
    # playback.pack(padx = 5)
    if (word == userWord):
        print("Correct!")
        # result.set("Correct!")
        response.configure(text = "Correct!")
    else:
        print("Not quite.")
        # result.set("Not quite.")
        response.configure(text = "Not quite!")
    return


def inputCategory():
    popup = Tk()
    popup.geometry("200x100")
    popup.title("Filter")
    filter = Entry(popup)
    filter.insert(0, "category")
    filter.pack(pady = 10)
    conf = Button(popup, text = "Confirm", command = lambda: displayDB(3, filter.get().lower()))
    conf.pack(pady = 10)

root = Tk()
root.title("MedPro")
root.geometry("500x500")
frame = Frame(root)
frame.pack()
terms = Listbox(frame, width = 30)
terms.pack(side = "left", fill = "y")
speedlbl = Label(frame, text = "Enter a value between 0.4 and 1.5\n to change playback speed.")
speedlbl.pack(side = "right", padx = 5)
speedbox = Entry(frame, width = 5)
speedbox.insert(0, "1.0")
speedbox.pack(side = "right", padx = 10)
frame3 = Frame(root)
frame3.pack()
input = Entry(frame3, width = 50)
input.pack(padx = 20, pady = 10, side = "left")
input.insert(0, "What word would you like to hear?")
confirm = Button(frame3, text = "Confirm", width = 10, height = 2, command = lambda: uiRun(input.get()))
confirm.pack(padx = 5, pady = 10, side = "left")

frame2 = Frame(root)
frame2.pack()
az = Button(frame2, text = "A-Z", width = 10, height = 2, command = lambda: displayDB(1, None))
az.pack(padx = 5, side = "left")
za = Button(frame2, text = "Z-A", width = 10, height = 2, command = lambda: displayDB(2, None))
za.pack(padx = 5, side = "left")
cate = Button(frame2, text = "Category", width = 10, height = 2, command = lambda: inputCategory())
cate.pack(padx = 5, side = "left")

frame4 = Frame(root)
frame4.pack()
exit = Button(frame4, text = "exit", width = 10, height = 2, command = lambda: sys.exit())
exit.pack(pady = 10)
ch = IntVar()
check = Checkbutton(frame4, text = "Clean audio? No feedback will be given.", variable = ch)
check.pack(side = "right", padx = 10, pady = 10)


run()