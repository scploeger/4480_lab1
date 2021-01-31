#By Spencer Ploeger
#Updated: Jan/30/2021
#ENGG*4480 Lab 1

#IMU library from: https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect
import sys
import os
import matplotlib
matplotlib.use('Agg') #use non-interactive backend (needed for matplotlib to run on pi) #must be called before importing pyplot
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
sys.path.append("")
import time
import pandas as pd
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250


config = 0 #for acceleromater scale setting input check
trial_num = "2" #for naming output files and labling graphs
my_dpi = 91 #monitor dpi for scaling images


#empty arrays for imu data
a = []
g = []
m = []

#Plot function
#parmeters: none
#returns: none
#this function plots Acceleration and Gyroscope values
def plot():
     #convert array of tuples to a numpy array
        a_data = np.array(a)
        g_data = np.array(g)
        m_data = np.array(m)

        #export the accelerometer and gyro data to CSV files
        np.savetxt('Trial ' + trial_num + ' - Accelerometer Data.csv', a, delimiter=",")
        np.savetxt('Trial ' + trial_num + ' - Gyroscope Data.csv', g, delimiter=",")

        #plot A graph
        plt.figure()
        plt.plot(a_data[:,0], label = "a_x") #plot the X, Y, Z data seperately
        plt.plot(a_data[:,1], label = "a_y")
        plt.plot(a_data[:,2], label = "a_z")
        plt.legend(loc="upper left")
        plt.ylim(-2.1, 2.1)
        plt.ylabel('Acceleration [g]')
        plt.xlabel('# Samples')
        plt.title('Trial ' + trial_num + ' - Accelerometer Data')
        plt.savefig('Trial ' + trial_num + ' - Accelerometer Data.png')

        # First, design the Butterworth filter
        plt.figure(figsize=(16, 10), dpi=my_dpi)
        
        N  = 3    # Filter order
        Wn = 0.1 # Cutoff frequency
        B, A = signal.butter(N, Wn, output='ba')
        smooth_data = signal.filtfilt(B,A, a_data[:,0])

        #Window moving average filtering with Pandas
        smooth_data_pandas = pd.Series(a_data[:,0]).rolling(window=7).mean()


        plt.plot(a_data[:,0],'r-', label = "original data") #plot original data
        plt.plot(smooth_data,'b-', label = "Butterworth Filter") #plot smoothed data butterworth
        plt.plot(smooth_data_pandas,'g-', label = "moving average") #plot smoothed data butterworth
        plt.legend(loc="upper left")
        plt.savefig('Filtered.png')

        #plot G graph
        plt.figure()
        plt.plot(g_data[:,0], label = "g_x") #plot the X, Y, Z data seperately
        plt.plot(g_data[:,1], label = "g_y")
        plt.plot(g_data[:,2], label = "g_z")
        plt.legend(loc="upper left")
        plt.ylim(-500, 500)
        plt.ylabel('Degrees per Seconds (dps)')
        plt.xlabel('# Samples')
        plt.title('Trial ' + trial_num + ' - Gyroscope Data')
        plt.savefig('Trial ' + trial_num + ' - Gyroscope Data.png')

#main function
def main(config):

    mpu = MPU9250(
    address_ak=AK8963_ADDRESS, 
    address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
    address_mpu_slave=None, 
    bus=1,
    afs=AFS_2G, #sensitivity defaults to 2G
    gfs=GFS_1000,
    mfs=AK8963_BIT_16, 
    mode=AK8963_MODE_C100HZ)

    num_samples = int(input("How many samples do you want to take?: (Enter int only) \n"))

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

        plot() #after collecting data, plot charts and export CSV files
    except KeyboardInterrupt: #if CTRL+C is pressed
        plot() #...still plot
        print('Interrupted')
        try: #then exit
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__ == "__main__":
    main(config)