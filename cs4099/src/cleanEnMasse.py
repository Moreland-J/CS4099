import os
import sys
import glob
import numpy
import subprocess
# import pydub
from pydub import AudioSegment
AudioSegment.converter = "C:\ffmpeg\bin"

SILENCE_FILE = "silence.wav"
SILENCE_PROF = "silence.prof"
SOX = "C:\Program Files (x86)\sox-14-4-2"

def printcom(str, level = 0):
    if level >= 2:
        print(str)

def findSilence(file):
    sound = AudioSegment.from_file(file, format = "wav")
    ms = 0
    current = 0
    longestTime = 50
    longestVal = None
    print("for")
    for i in sound:
        if i.dBFS > -38.0:
            length = ms - current
            # print("ms:" + str(ms) + "\tcurrent: " + str(current) + "\tlength: " + str(length))
            if length > longestTime:
                print("set")
                longestVal = sound[current : ms]
                longestTime = length
            current = ms + 1
        ms += 1

    print("longest")
    printcom("longest segment " + str(longestTime / 1000) + " seconds", 2)
    longestVal[200 : -200].export(SILENCE_FILE, format = "wav")
    print("value set")

def soxDenoise(file):
    print("sox")
    sound = AudioSegment.from_file(SILENCE_FILE, format = "wav")
    length = len(sound) / 1000.0
    # CALL SOX ON SILENCE STORED AND TRIM THAT SILENCE FROM THE LENGTH
    command = '{sox} "{input}" -n trim 0 {len} noiseprof {prof}'.format(sox = SOX, input = SILENCE_FILE, len = length, prof = SILENCE_PROF)
    print(command)
    subprocess.call(command)

    out = os.path.join(os.path.dirname(file), "cleaned", os.path.basename(file))
    if not os.path.exists(os.path.dirname(out)):
        os.makedirs(os.path.dirname(out))
        
    command = '{sox} "{file}" "{out}" noisered {prof} 0.3'.format(sox = SOX, file = SILENCE_FILE, prof = SILENCE_PROF)
    print(command)
    subprocess.call(command)


# DELETE BACKGROUND "SILENCE" FILES
def cleanup():
    os.remove(SILENCE_FILE)
    os.remove(SILENCE_PROF)


def doActions(actions, params):
    createFiles()
    list = glob.glob(os.path.join(params["root"], "*.wav"))
    count = 1
    print(list)
    for file in list:
        printcom("[{}/{}] Processing : {}".format(count, len(list), file), 4)
        count += 1
        print("find silence")
        if "find_silence" in actions:
            findSilence(file)
        if "sox_denoise" in actions:
            soxDenoise(file)
    if "cleanup" in actions:
        cleanup()

def actOnce(actions, file):
    try:
        createFiles()
        if "find_silence" in actions:
                findSilence(file)
        if "sox_denoise" in actions:
            soxDenoise(file)
        if "cleanup" in actions:
            cleanup()
    except FileNotFoundError as e:
        print(e)
        return

def createFiles():
    try:
        f = open(SILENCE_FILE, "x")
    except Exception:
        print("file exists")

    try:
        f = open(SILENCE_PROF, "x")
    except Exception:
        print("profile exists")

if __name__ == '__main__':
    print("started")
    actions = ["find_silence", "sox_denoise", "cleanup", "nothing"]
    params = { "root" : sys.argv[1], "nothing" : None }
    doActions(actions, params)
    print("finished")
    sys.exit(0)