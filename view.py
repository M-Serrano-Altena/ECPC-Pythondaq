# Marc Serrano Altena
# 06-11-2023
# views the data from the model experiment and makes a csv file and shows a I,U graph of the LED

from diode_experimtent import DiodeExperiment, list_devices, device
from random import *
import matplotlib.pyplot as plt
import csv
import numpy as np

# U0 has the full current
# U1 measures the current passing through the LED and resistor, which is the full current
# U2 measures the current passing through the resistor

def view_data(device):
    voltage_scans = []
    currents_scans = []

    for _ in range(0, 10):
        diode = DiodeExperiment(device)
        diode.scan(start=0, stop=1023)
        voltage_scans.append(diode.voltage_list)
        currents_scans.append(diode.current_list)

    print(voltage_scans)
    average_voltage_list = [np.average(((volt1, volt2, volt3, volt4, volt5, volt6, volt7, volt8, volt9, volt10))) for volt1, volt2, volt3, volt4, volt5, volt6, volt7, volt8, volt9, volt10 in zip(voltage_scans[0], voltage_scans[1], voltage_scans[2], voltage_scans[3], voltage_scans[4], voltage_scans[5], voltage_scans[6], voltage_scans[7], voltage_scans[8], voltage_scans[9])]
    average_current_list = [np.average((current1, current2, current3, current4, current5, current6, current7, current8, current9, current10)) for current1, current2, current3, current4, current5, current6, current7, current8, current9, current10 in zip(voltage_scans[0], voltage_scans[1], voltage_scans[2], voltage_scans[3], voltage_scans[4], voltage_scans[5], voltage_scans[6], voltage_scans[7], voltage_scans[8], voltage_scans[9])]
    # write the I,U data to a csv
    with open("metingen.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['U', 'I'])
        for voltage, current in zip(diode.voltage_list, diode.current_list):
            writer.writerow([voltage, current])    

    # plot (I, U) diagram of the LED
    plt.figure()

    plt.xlim(0, 3.0)
    plt.ylim(0, 0.0025)
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (A)")
    plt.scatter(diode.voltage_list, diode.current_list, s=5, c='blue')

    plt.show()
    return

view_data(device)
