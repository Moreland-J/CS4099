import matplotlib.pyplot as plt
import numpy as np
import wave
import scipy.fftpack as sf
import scipy.signal as sig
from scipy import signal
from scipy.io import wavfile
from scipy.io.wavfile import read
from scipy.io.wavfile import write

class CompTool():
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

    def clean(self):
        print("clean")
        '''
        # USE WAVE
        attemptWav = wave.open("out.wav", "r")
        # EXTRACT RAW AUDIO FROM .WAV FILE
        attemptAud = attemptWav.readframes(-1)
        attemptAud = np.fromstring(attemptAud, "Int16")
        plt.plot(attemptAud)
        plt.show()
        

        fs = 100
        xf = abs(sf.fft(attemptAud))
        length = np.size(attemptAud)
        freq = (fs / 2) * np.linspace(0, 1, length / 2)
        xm = (2 / 1) * abs(xf[0:np.size(freq)])

        b, a = signal.butter(4, 100, 'low', analog = True)
        w, h = signal.freqs(b, a)
        plt.figure(1)
        plt.title("Attempt")
        plt.plot(attemptAud)
        plt.semilogx(w, 20 * np.log10(abs(h)))
        plt.show()
        attemptWav.close()
        '''

        freq, array = read("database/" + self.word + ".wav")
        plt.subplot(3, 2, 1)
        plt.plot(array)
        plt.title("Original")
        plt.ylabel("Amplitude")

        print("point reached")
        plt.subplot(3, 2, 2)
        b, a = signal.butter(5, 1000/(freq / 2), btype = 'highpass')
        filtered1 = signal.lfilter(b, a, array)
        plt.plot(filtered1)
        plt.title("Cleaned High")
        plt.ylabel("Amplitude")

        plt.subplot(3, 2, 3)
        c, d = signal.butter(5, 380 / (freq / 2), btype = 'lowpass')
        filtered1 = signal.lfilter(c, d, filtered1)
        plt.plot(filtered1)
        plt.title("Cleaned Low")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")

        freq, array = read("out.wav")
        plt.subplot(3, 2, 4)
        plt.plot(array)
        plt.title("Attempt")
        plt.ylabel("Amplitude")

        plt.subplot(3, 2, 5)
        b, a = signal.butter(5, 1000/(freq / 2), btype = 'highpass')
        filtered = signal.lfilter(b, a, array)
        plt.plot(filtered)
        plt.title("Cleaned High")
        plt.ylabel("Amplitude")

        plt.subplot(3, 2, 6)
        c, d = signal.butter(5, 380 / (freq / 2), btype = 'lowpass')
        filtered = signal.lfilter(c, d, filtered)
        plt.plot(filtered)
        plt.title("Cleaned Low")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")

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