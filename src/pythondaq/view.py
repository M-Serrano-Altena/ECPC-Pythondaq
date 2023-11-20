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

def view_data(device, filename, voltage_input_start, voltage_input_end):
    """shows the data from the diode experiment in a (I,U) diagram and exports the current and voltage to a csv file

    Args:
        device (ArduinoVISADevice): class instance that gives commands to the arduino
        filename (string): name of the file to export the data as a csv file
        voltage_input_start (float): start voltage of the input in the arduino
        voltage_input_end (float): end voltage of the input in the arduino
    """    
    diode = DiodeExperiment(device)
    digital_value_start = device.analog_to_digital(voltage_input_start)
    digital_value_end = device.analog_to_digital(voltage_input_end)
    diode.average_value_scan(start=digital_value_start, stop=digital_value_end, measurement_amount=1)
    
    # write the I,U data to a csv
    with open(f"{filename}.csv", "w", newline="") as csvfile:
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

def main(filename, voltage_input_start, voltage_input_end):
    """makes a connection with the arduino and runs the view_data function
    """
    arduino_port =  "ASRL5::INSTR"   
    device = make_connection(arduino_port=arduino_port)
    view_data(device, filename, voltage_input_start, voltage_input_end)

if __name__ == "__main__":
    main()   