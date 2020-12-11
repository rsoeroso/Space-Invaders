from ECE16Lib.CircularList import CircularList
import ECE16Lib.DSP as filt
import numpy as np

class Orientation:
    __orientation = "" #output orientation
    __x0 = 1800 #normalization values (set these as apropriate for hardware)
    __y0 = 1800
    __z0 = 2250
    __ax = None #list of accelerometer values
    __ay = None
    __az = None
    __thresh1 = 300 #sensitivity ratings
    __thresh2 = 200
    __thresh3 = 100
    __times = None #associated timestamps
    __num_samples = 0  # The length of data maintained in memory for threshold recalculation
    __adjust_timer = 0
    __fs = 0           # Sampling rate in Hz

    def __init__(self,num_samples, fs, times=[], datax=[], datay=[], dataz=[]):
        self.__num_samples = num_samples
        self.__fs = fs
        self.__ax = CircularList(datax, num_samples)
        self.__ay = CircularList(datay, num_samples)
        self.__az = CircularList(dataz, num_samples)
        self.__times = CircularList(times, num_samples)
        self.__thresh1 = 0.75*(self.__z0 - self.__x0)
        self.__thresh2 = 0.5*(self.__z0 - self.__x0)
        self.__thresh3 = 0.25*(self.__z0 - self.__x0)

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
        self.__ax.add(x-self.__x0) #normalize values so that 0 is horizontal
        self.__ay.add(y-self.__y0)
        self.__az.add(z-self.__z0)


    def process(self):
        #extract average values from circularlists
        x_arr = np.array(self.__ax)
        x_last = x_arr[-1]
        y_arr = np.array(self.__ay)
        y_last = y_arr[-1]
        z_arr = np.array(self.__az)
        z_last = z_arr[-1]
        thresh1 = self.__thresh1
        thresh2 = self.__thresh2
        thresh3 = self.__thresh3
        command = "NONE"
        #detect x wise incline
        if ((abs(x_last)>abs(y_last)) or (abs(x_last)>abs(z_last))): #if x deviation is greater than either y deviation or z deviation
        #note: delta abs(x) = delta abs(y) + delta abs(z) since gravitational acceleration is more or less a constant
        # if this condition does not trigger: either the controller hasn't moved, or it rotated around x axis
            if (x_last>thresh1):
                command = "RIGHTH"
            elif(x_last>thresh2):
                command = "RIGHTM"
            elif(x_last>thresh3):
                command = "RIGHTL"
            elif(x_last>(-thresh3)):
                command = "NONE"
            elif(x_last>(-thresh2)):
                command = "LEFTL"
            elif(x_last>(-thresh1)):
                command = "LEFTM"
            else:
                command = "LEFTH"

        self.__orientation = command

        #adjust normalization values if needed
        if(self.__adjust_timer>=self.__num_samples):
            x_avg = np.mean(x_arr)
            y_avg = np.mean(y_arr)
            z_avg = np.mean(z_arr)
            self.__x0 = self.__x0 + 0.5*x_avg #adjust normalization value
            x_arr = x_arr - 0.5*x_avg #adjust stored memory
            self.__ax.add(x_arr.tolist()) #flush old memory values
            self.__y0 = self.__y0 + 0.5*y_avg
            y_arr = y_arr - 0.5*y_avg
            self.__ay.add(y_arr.tolist())
            self.__z0 = self.__z0 + 0.5*z_avg
            z_arr = z_arr - 0.5*z_avg
            self.__az.add(z_arr.tolist())
            #recompute thresholds
            self.__thresh1 = 0.75*(self.__z0 - self.__x0)
            self.__thresh2 = 0.5*(self.__z0 - self.__x0)
            self.__thresh3 = 0.25*(self.__z0 - self.__x0)

            self.__adjust_timer = 0
        else:
            self.__adjust_timer = self.__adjust_timer+1

    def get_orientation(self):
        return self.__orientation