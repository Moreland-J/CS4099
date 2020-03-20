import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile

class CompTool():
    def __init__(self, root, new, word):
        self.root = root 
        # The original word
        self.new = new
        self.word = word
        # How many morphemes should be used as the prefix for the new portmanteau
        self.output = '' #
        self.compare()

    def compare(self):
        recording = self.root
        attempt = self.new
        word = self.word
        sample_rate, samples = wavfile.read("database/" + word + ".wav")
        frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)

        plt.pcolormesh(times, frequencies, spectrogram)
        plt.imshow(spectrogram)
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
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