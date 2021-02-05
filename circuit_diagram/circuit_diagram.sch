EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 1 1
Title "ENGG*4480 Lab 1 Circuit Diagram"
Date "2021-02-05"
Rev "1"
Comp "Group 1"
Comment1 "G. Black, M. Bolan, L. Dasovic, S. Ploeger"
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Connector:Raspberry_Pi_2_3 J1
U 1 1 601D5AB9
P 3850 4000
F 0 "J1" H 4500 5250 50  0000 C CNN
F 1 "Raspberry_Pi_2_3" H 3250 5250 50  0000 C CNN
F 2 "" H 3850 4000 50  0001 C CNN
F 3 "https://www.raspberrypi.org/documentation/hardware/raspberrypi/schematics/rpi_SCH_3bplus_1p0_reduced.pdf" H 3850 4000 50  0001 C CNN
	1    3850 4000
	1    0    0    -1  
$EndComp
$Comp
L Sensor_Motion:MPU-9250 U1
U 1 1 601D8346
P 6200 3650
F 0 "U1" H 6650 2900 50  0000 C CNN
F 1 "MPU-9250" H 5900 2900 50  0000 C CNN
F 2 "Sensor_Motion:InvenSense_QFN-24_3x3mm_P0.4mm" H 6200 2650 50  0001 C CNN
F 3 "https://store.invensense.com/datasheets/invensense/MPU9250REV1.0.pdf" H 6200 3500 50  0001 C CNN
	1    6200 3650
	1    0    0    -1  
$EndComp
Wire Wire Line
	6200 4550 6200 5400
Wire Wire Line
	6200 5400 4150 5400
Wire Wire Line
	4150 5400 4150 5300
Wire Wire Line
	4050 2700 4050 2350
Wire Wire Line
	4050 2350 6300 2350
Wire Wire Line
	6300 2350 6300 2750
Wire Wire Line
	4650 3400 5100 3400
Wire Wire Line
	5100 3400 5100 3350
Wire Wire Line
	5100 3350 5500 3350
Wire Wire Line
	4650 3500 5100 3500
Wire Wire Line
	5100 3500 5100 3550
Wire Wire Line
	5100 3550 5500 3550
Text Notes 4550 5250 0    98   ~ 20
Raspberry Pi 4\nGPIO
Text Notes 5550 2800 0    98   ~ 20
MPU9250\nIMU
$EndSCHEMATC
