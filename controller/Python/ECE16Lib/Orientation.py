from ECE16Lib.CircularList import CircularList
import ECE16Lib.DSP as filt
import numpy as np

class Orientation:
    __orientation = ""
    __ax = None
    __ay = None
    __az = None
    __times = None
    __num_samples = 0  # The length of data maintained
    __new_samples = 0  # How many new samples exist to process
    __fs = 0           # Sampling rate in Hz

    def __init__(self,num_samples, fs, times=[], datax=[], datay=[], dataz=[]):
        self.__num_samples = num_samples
        self.__fs = fs
        self.__ax = CircularList(datax, num_samples)
        self.__ay = CircularList(datay, num_samples)
        self.__az = CircularList(dataz, num_samples)
        self.__times = self.__ax = CircularList(times, num_samples)

    def add(self, t, x, y, z):
        if isinstance(t, np.ndarray):
            t = t.tolist()
        if isinstance(x, np.ndarray):
            x = x.tolist()
        if isinstance(t, np.ndarray):
            y = y.tolist()
        if isinstance(x, np.ndarray):
            z = z.tolist()

        self.__times.add(t)
        self.__ax.add(x)
        self.__ay.add(y)
        self.__az.add(z)
        self.__new_samples += len(x)

    def get_orientation(self):
        ## TODO:
