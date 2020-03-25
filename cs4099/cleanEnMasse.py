import os
import glob
import numpy
from pydub import AudioSegment

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
    longestTime = 500
    longestVal = None
    for i in sound:
        if i.dBFS > -38.00:
            length = ms - current
            if length > longestTime:
                longestVal = sound[current : ms]
                longestTime = length
            current = ms + 1
        ms += 1
    longestVal[200 : -200].export(SILENCE_FILE, format = "wav")

def soxDenoise(file):
    sound = AudioSegment.from_file(SILENCE_FILE, format = "wav")
    length = len(sound) / 1000.0
    # CALL SOX ON SILENCE STORED AND TRIM THAT SILENCE FROM THE LENGTH
    command = '{sox} "{file}" -n trim 0 {len} noiseprof {prof}'.format(sox = SOX, file = SILENCE_FILE, len = length, prof = SILENCE_PROF)
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
    list = glob.glob(os.path.join(params["root"], ".wav"))
    count = 1
    for file in list:
        count += 1
        if "find_silence" in actions:
            findSilence(file)
        if "sox_denoise" in actions:
            soxDenoise(file)
    if "cleanup" in actions:
        cleanup()

if __name__ == '__main__':
    actions = ["find_silence", "sox_denoise", "cleanup", "nothing"]
    params = { "root" : sys.argv[1], "nothing" : None }
    doActions(actions, params)
    sys.exit(0)