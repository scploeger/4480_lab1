#By Spencer Ploeger
#Updated: Jan/30/2021
#ENGG*4480 Lab 1

#IMU library from: https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect
#IMU library functions: https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect/blob/master/mpu9250_jmdev/mpu_9250.py#L64
import sys #access functions strongly connected to python interpreter
import os #provides access to system variables, file names, paths, etc
import matplotlib #used for plotting sensor data
matplotlib.use('Agg') #use non-interactive backend (needed for matplotlib to run on pi) #must be called before importing pyplot
import matplotlib.pyplot as plt #for plotting graphs
import numpy as np #for creating the dynamic arrays of sensor data
import scipy.signal as signal #for filtering
sys.path.append("") #references parent directory
#import time #for making delays/pauses
import pandas as pd #for window filtering
from mpu9250_jmdev.registers import * #required for IMU use
from mpu9250_jmdev.mpu_9250 import MPU9250 #IMU library


config = 0 #for acceleromater scale setting input check
trial_num = "1" #for naming output files and labling graphs
my_dpi = 91 #monitor dpi for scaling images
filtering = "n" #defult plotting filtered graphs NO


#empty arrays for imu data
a = []
g = []
m = []

#Plot function
#parmeters: none
#returns: none
#this function plots Acceleration and Gyroscope values
def plot(filtering):
     #convert array of tuples to a numpy array
        a_data = np.array(a)
        g_data = np.array(g)
        m_data = np.array(m)

        #export the accelerometer and gyro data to CSV files
        np.savetxt('Trial ' + trial_num + ' - Accelerometer Data.csv', a, delimiter=",")
        np.savetxt('Trial ' + trial_num + ' - Gyroscope Data.csv', g, delimiter=",")

        #plot Acceleromater graph
        plt.figure(figsize=(16, 10), dpi=my_dpi)
        plt.plot(a_data[:,0], label = "a_x") #plot the X, Y, Z data seperately
        plt.plot(a_data[:,1], label = "a_y")
        plt.plot(a_data[:,2], label = "a_z")
        plt.legend(loc="upper left")
        plt.ylim(-4.1, 4.1)
        plt.ylabel('Acceleration [g]')
        plt.xlabel('# Samples')
        plt.title('Trial ' + trial_num + ' - Accelerometer Data')
        plt.savefig('Trial ' + trial_num + ' - Accelerometer Data.png')

        #plot G graph
        plt.figure(figsize=(16, 10), dpi=my_dpi)
        plt.plot(g_data[:,0], label = "g_x") #plot the X, Y, Z data seperately
        plt.plot(g_data[:,1], label = "g_y")
        plt.plot(g_data[:,2], label = "g_z")
        plt.legend(loc="upper left")
        plt.ylim(-1200, 1200)
        plt.ylabel('Degrees per Seconds (dps)')
        plt.xlabel('# Samples')
        plt.title('Trial ' + trial_num + ' - Gyroscope Data')
        plt.savefig('Trial ' + trial_num + ' - Gyroscope Data.png')

        if(filtering == 'y'):
            #plot the filtered Accelerometer data (accelerometer X axis)
            plt.figure(figsize=(16, 10), dpi=my_dpi)
            # First, design the Butterworth filter
            N  = 3    # Filter order
            Wn = 0.5 # Cutoff frequency
            B, A = signal.butter(N, Wn, output='ba')
            smooth_data_05 = signal.filtfilt(B,A, a_data[:,0])

            # First, design the Butterworth filter
            N  = 3    # Filter order
            Wn = 0.1 # Cutoff frequency
            B, A = signal.butter(N, Wn, output='ba')
            smooth_data_01 = signal.filtfilt(B,A, a_data[:,0])

            #Window moving average filtering with Pandas
            smooth_data_pandas = pd.Series(a_data[:,0]).rolling(window=7).mean()

            plt.plot(a_data[:,0],'r-', label = "Raw data") #plot original data (Accleromter X Data)
            plt.plot(smooth_data_01,'b-', label = "Butterworth filter, wn = 0.1, order = 3") #plot smoothed data butterworth
            plt.plot(smooth_data_05,'y-', label = "Butterworth filter, wn = 0.5, order = 3") #plot smoothed data butterworth
            plt.plot(smooth_data_pandas,'g-', label = "Moving average, window size = 7") #plot smoothed data moving average
            plt.legend(loc="upper left")
            plt.ylabel('Acceleration [g]')
            plt.xlabel('# Samples')
            plt.title('Accelerometer Data (X-Axis) Filter Comparison (Trial ' + trial_num + ')')
            plt.savefig('Accelerometer Data (X-Axis) Filter Comparison (Trial ' + trial_num + ').png')


            #plot the filtered Gyro data (Gyroscope Y axis)
            plt.figure(figsize=(16, 10), dpi=my_dpi)
            # First, design the Butterworth filter
            N  = 3    # Filter order
            Wn = 0.1 # Cutoff frequency
            B, A = signal.butter(N, Wn, output='ba')
            smooth_data_3 = signal.filtfilt(B,A, g_data[:,1])

            # First, design the Butterworth filter
            N  = 5    # Filter order
            Wn = 0.1 # Cutoff frequency
            B, A = signal.butter(N, Wn, output='ba')
            smooth_data_5 = signal.filtfilt(B,A, g_data[:,1])

            #Window moving average filtering with Pandas
            smooth_data_pandas = pd.Series(g_data[:,1]).rolling(window=7).mean()

            plt.plot(g_data[:,1],'r-', label = "Raw data") #plot original data (Accleromter X Data)
            plt.plot(smooth_data_3,'b-', label = "Butterworth filter, wn = 0.1, order = 3") #plot smoothed data butterworth
            plt.plot(smooth_data_5,'y-', label = "Butterworth filter, wn = 0.1, order = 5") #plot smoothed data butterworth
            plt.plot(smooth_data_pandas,'g-', label = "Moving average, window size = 7") #plot smoothed data moving average
            plt.legend(loc="upper left")
            plt.ylabel('Degrees per Seconds (dps)')
            plt.xlabel('# Samples')
            plt.title('Gyroscope Data (Y-Axis) Filter Comparison (Trial ' + trial_num + ')')
            plt.savefig('Gyroscope Data (Y-Axis) Filter Comparison (Trial ' + trial_num + ').png' )

#main function
def main(config):

    #mpu object constructor
    # @param [in] self - The object pointer.
    # @param [in] address_ak - AK8963 I2C slave address (default:AK8963_ADDRESS[0x0C]).
    # @param [in] address_mpu_master - MPU-9250 I2C address (default:MPU9050_ADDRESS_68[0x68]).
    # @param [in] address_mpu_slave - MPU-9250 I2C slave address (default:[None]).
    # @param [in] bus - I2C bus board (default:Board Revision 2[1]).
    # @param [in] gfs - Gyroscope full scale select (default:GFS_2000[2000dps]).
    # @param [in] afs - Accelerometer full scale select (default:AFS_16G[16g]).
    # @param [in] mfs - Magnetometer scale select (default:AK8963_BIT_16[16bit])
    # @param [in] mode - Magnetometer mode select (default:AK8963_MODE_C100HZ[Continous 100Hz])
    mpu = MPU9250(
    address_ak=AK8963_ADDRESS, 
    address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
    address_mpu_slave=None, #we are only using one I2C Sensor
    bus=1, #select I2C bus, PI has multiple
    afs=AFS_2G, #(accel. full scale) sensitivity defaults to 2G
    gfs=GFS_1000, #gyro full scale (defaults to 1000dps)
    mfs=AK8963_BIT_16, #(magnometer scale select) defaults to 16bit
    mode=AK8963_MODE_C100HZ) #magnometer scale select

    num_samples = int(input("How many samples do you want to take?: (Enter int only) \n"))
    filtering = input("Would you like to plot filtered graphs too? (Enter 'y' or 'n' only!) \n")

    while(config == 0):
        itr = 0
        print("What accelerometer scale modifer do you want to use?")
        val = input("Press: (2)_G, (4)_G, (8)_G, 1(6)_G\n")

        if(val != '2' and val != '4' and val != '8' and val != '6'):
            print("Only enter 2, 4, 8, or 1!")
        else:
            #set the desired accelerometer scaler
            if val == '2':
                setattr(mpu, 'afs', AFS_2G)
            elif val == '4':
                setattr(mpu, 'afs', AFS_4G)
            elif val == '8':
                setattr(mpu, 'afs', AFS_8G)
            elif val == '6':
                setattr(mpu, 'afs', AFS_16G)

            config = 1

    mpu.configure() #write settings to imu registers
    print(mpu.getAllSettings()) #print settings to confirm they are correct

    try:
        while(itr < num_samples):#iterate until desired number of samples is reached
            a.append(mpu.readAccelerometerMaster()) #append values read from IMU to respective array
            g.append(mpu.readGyroscopeMaster())
            m.append(mpu.readMagnetometerMaster())

            print("Accelerometer", a[len(a)-1]) #print the most recent values
            print("Gyroscope", g[len(g)-1])
            print("Magnetometer", g[len(g)-1])
            #print("Temperature", mpu.readTemperatureMaster())
            print("\n")

            itr += 1

        plot(filtering) #after collecting data, plot charts and export CSV files
    except KeyboardInterrupt: #if CTRL+C is pressed
        plot(filtering) #...still plot
        print('Interrupted')
        try: #then exit
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__ == "__main__":
    main(config)