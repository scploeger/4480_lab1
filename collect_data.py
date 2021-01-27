#from: https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect
import sys
import os
import matplotlib
matplotlib.use('Agg') #use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
sys.path.append("")

import time
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

config = 0
trial_num = "2"

#mpu.configure() # Apply the settings to the registers.

#empty array for ay
a = []
g = []
m = []


def plot():
     #convert array of tuples to a numpy array
        a_data = np.array(a)
        g_data = np.array(g)
        m_data = np.array(m)

        np.savetxt('Trial ' + trial_num + ' - Accelerometer Data.csv', a, delimiter=",")
        np.savetxt('Trial ' + trial_num + ' - Gyroscope Data.csv', g, delimiter=",")

        #plot A graph
        plt.figure()
        plt.plot(a_data[:,0], label = "a_x")
        plt.plot(a_data[:,1], label = "a_y")
        plt.plot(a_data[:,2], label = "a_z")
        plt.legend(loc="upper left")
        plt.ylim(-2.1, 2.1)
        plt.ylabel('Acceleration [g]')
        plt.xlabel('# Samples')
        plt.title('Trial ' + trial_num + ' - Accelerometer Data')
        plt.savefig('Trial ' + trial_num + ' - Accelerometer Data.png')

        #plot G graph
        plt.figure()
        plt.plot(g_data[:,0], label = "g_x")
        plt.plot(g_data[:,1], label = "g_y")
        plt.plot(g_data[:,2], label = "g_z")
        plt.legend(loc="upper left")
        plt.ylim(-500, 500)
        plt.ylabel('Degrees per Seconds (dps)')
        plt.xlabel('# Samples')
        plt.title('Trial ' + trial_num + ' - Gyroscope Data')
        plt.savefig('Trial ' + trial_num + ' - Gyroscope Data.png')


def main(config):
    num_samples = int(input("How many samples do you want to take?: (Enter int only) \n"))

    while(config == 0):
        itr = 0
        print("What accelerometer scale modifer do you want to use?")
        val = input("Press: (2)_G, (4)_G, (8)_G, 1(6)_G\n")

        if(val != '2' and val != '4' and val != '8' and val != '6'):
            print("Only enter 2, 4, 8, or 1!")
        else:
            sensitivity = "AFS_" + val + "G"
            print("Sens: " + sensitivity)
            config = 1

    mpu = MPU9250(
    address_ak=AK8963_ADDRESS, 
    address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
    address_mpu_slave=None, 
    bus=1,
    afs=AFS_2G,
    gfs=GFS_1000,
    mfs=AK8963_BIT_16, 
    mode=AK8963_MODE_C100HZ)

    setattr(mpu, 'afs', AFS_8G)

    mpu.configure()

    print(mpu.getAllSettings())

    try:
        while(itr < num_samples):
            a.append(mpu.readAccelerometerMaster())
            g.append(mpu.readGyroscopeMaster())
            m.append(mpu.readMagnetometerMaster())

            print("Accelerometer", a[len(a)-1])
            print("Gyroscope", g[len(g)-1])
            print("Magnetometer", g[len(g)-1])
            #print("Temperature", mpu.readTemperatureMaster())
            print("\n")

            itr += 1

            time.sleep(0.1)
        plot()
    except KeyboardInterrupt:
        plot()
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__ == "__main__":
    main(config)