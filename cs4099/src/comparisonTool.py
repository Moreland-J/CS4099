import os
import matplotlib.pyplot as plt
import numpy as np
import wave
import soundfile as sf
import scipy.fftpack as fft
import scipy.signal as sig
from scipy import signal
from scipy.io import wavfile
from scipy.io.wavfile import read
from scipy.io.wavfile import write
import sounddevice as sd
import cleanEnMasse

class CompTool():
    cleanOriginal = None
    cleanAttempt = None

    def __init__(self, attempt, word):
        # The original word
        self.attempt = attempt
        self.word = word
        # How many morphemes should be used as the prefix for the new portmanteau
        self.output = '' #
        self.compare()

    def compare(self):
        # REMOVE BACKGROUND NOISE
        self.clean()
        self.spectrogram()

    def clean(self):
        # CLEAN THE ORIGINAL
        freq, array = read("../database/" + self.word + ".wav")
        plt.subplot(2, 2, 1)
        plt.plot(array)
        plt.title("Original")
        plt.ylabel("Amplitude")
        # HIGH PASS FILTER
        b, a = signal.butter(5, 1000/(freq / 2), btype = 'highpass')
        filtered1 = signal.lfilter(b, a, array)
        # LOW PASS FILTER
        plt.subplot(2, 2, 3)
        c, d = signal.butter(5, 380 / (freq / 2), btype = 'lowpass')
        filtered2 = signal.lfilter(c, d, filtered1)
        plt.plot(filtered2)
        plt.title("Cleaned Low")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")

        # CLEAN THE ATTEMPT
        freq, array = read("out.wav")
        plt.subplot(2, 2, 2)
        plt.plot(array)
        plt.title("Attempt")
        plt.ylabel("Amplitude")
        # HIGH PASS FILTER
        b, a = signal.butter(5, 1000/(freq / 2), btype = 'highpass')
        filtered3 = signal.lfilter(b, a, array)
        # LOW PASS THE HIGH PASS
        plt.subplot(2, 2, 4)
        c, d = signal.butter(5, 380 / (freq / 2), btype = 'lowpass')
        filtered4 = signal.lfilter(c, d, filtered3)
        plt.plot(filtered4)
        plt.title("Cleaned Low")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")

        # ASSIGN GLOBAL VARIABLES
        self.cleanOriginal = filtered2        
        self.cleanAttempt = filtered4
        # WRITE .WAV OF CLEANED
        # TODO: DELETE
        fs = 16000
        filename = "clean.wav"
        sf.write(filename, self.cleanAttempt, fs)

        print("clean mass")
        self.finalClean()
        print("finish")

        plt.show()
        os.remove(filename)

    def finalClean(self):
        cleanEnMasse.actOnce(actions = ["find_silence", "sox_denoise", "cleanup", "nothing"], file = "clean.wav")

    def spectrogram(self):
        dt = 0.0005
        t = np.arange(0, 20, dt)
        s1 = np.sin(2 * np.pi * 100 * t)
        s2 = 2 * np.sin(2 * np.pi * 400 * t)
        s2 = s2 * self.cleanAttempt

        x = s1 + s2 + self.cleanAttempt
        nfft = 1024
        fs = int(1.0 / dt)

        ax1 = plt.sublplot(2, 1, 1)
        plt.plot(t, x)
        plt.subplot(2, 1, 2, sharex = ax1)
        pxx, freqs, bins, im = plt.specgram(x, NFFT = nfft, Fs = fs, noverlap = 900)
        plt.show()

# STEP 1
# eliminate background noise
# use: scipy

'''
# STEP 2
# distance metric
# compares two speech patterns
# .1 - spectogram of audio
# .2 - represent w/ 2D array
# use: OpenCV
        blob detection (the big vocal area)
# .3 - normalize two blob (speed adapt)
# .4 - normalize by intensity also (volume accounted for)
'''

'''
# STEP 3
# direct comparison time
# various methods possible
# opt 1 - cosine
# opt 2 - subtraction
# set difference threshold and see if it meets
'''