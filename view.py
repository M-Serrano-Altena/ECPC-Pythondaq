# Marc Serrano Altena
# 06-11-2023
# views the data from the model experiment and makes a csv file and shows a I,U graph of the LED

from diode_experiment import *
import matplotlib.pyplot as plt
import csv

# U0 has the full current
# U1 measures the current passing through the LED and resistor, which is the full current
# U2 measures the current passing through the resistor

def view_data(device):
    diode = DiodeExperiment(device)
    diode.average_value_scan(start=0, stop=1023)

    # write the I,U data to a csv
    with open("metingen.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['U', 'I'])
        for voltage, current in zip(diode.average_voltage_list, diode.average_current_list):
            writer.writerow([voltage, current])    

    # plot (I, U) diagram of the LED
    plt.figure()

    plt.xlim(0, 3.0)
    plt.ylim(0, 0.0025)
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (A)")
    plt.errorbar(diode.average_voltage_list, diode.average_current_list, xerr=diode.error_voltage_list, yerr=diode.error_current_list, fmt='bo-', ecolor='k')

    plt.show()
    return

view_data(device)
