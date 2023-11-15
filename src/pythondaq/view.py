# Marc Serrano Altena
# 06-11-2023
# views the data from the model experiment and makes a csv file and shows a I,U graph of the LED

from pythondaq.diode_experiment import *
import matplotlib.pyplot as plt
import csv
# import os 

## output channel meaning:
# U0 has the full current
# U1 measures the current passing through the LED and resistor, which is the full current minus some loss to the wires
# U2 measures the current passing through the resistor

# shows the data from the diode experiment in a (I,U) diagram and exports the I and U values in a csv file
def view_data(device):
    diode = DiodeExperiment(device)
    diode.average_value_scan(start=0, stop=1023, measurement_amount=10)

    # # to make a new csv file for a different measurement
    num = 1 
    # while os.path.isfile(f"metingen-{num}.csv"):
    #     num += 1
    
    # write the I,U data to a csv
    with open(f"metingen-{num}.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["U", "I", "U error", "I error"])
        for voltage, current, voltage_error, current_error  in zip(
            diode.average_voltage_list, diode.average_current_list, diode.error_voltage_list, diode.error_current_list
        ):
            writer.writerow([voltage, current, voltage_error, current_error])


    # plot (I, U) diagram of the LED
    plt.figure()

    plt.xlim(0, 3.0)
    plt.ylim(0, 0.0025)
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (A)")
    plt.errorbar(
        diode.average_voltage_list,
        diode.average_current_list,
        xerr=diode.error_voltage_list,
        yerr=diode.error_current_list,
        fmt="bo-",
        ecolor="k",
        markersize=3,
    )

    plt.show()
    return

def main():
    device = make_connection()
    view_data(device)

if __name__ == "__main__":
    main()   