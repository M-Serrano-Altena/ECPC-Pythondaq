from arduino_device import ArduinoVISADevice, list_devices
from random import *
import matplotlib.pyplot as plt
import csv

device = ArduinoVISADevice(port = "ASRL5::INSTR")

# U0 has the full current
# U1 measures the current passing through the LED and resistor, which is the full current
# U2 measures the current passing through the resistor

# voltage increases till the max intensity
def volt_increase(device):
    resistance = 220 #ohm
    l_voltage = []
    l_current = []

    # 1023 is de max output, 1024 gives a voltage of 0
    for adc_tot in range(0, 1024): 
        device.set_output_value(adc_tot)
        voltage_tot = device.get_input_value_voltage(channel=1)
        voltage_r = device.get_input_value_voltage(channel=2)
        voltage_led = voltage_tot - voltage_r
        current = voltage_r/resistance

        l_voltage.append(voltage_led)
        l_current.append(current)

    with open("metingen.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['U', 'I'])
        for voltage, current in zip(l_voltage, l_current):
            writer.writerow([voltage, current])

    # to turn of LED after experiment
    device.set_output_value(0)    

    fig = plt.figure()

    plt.xlim(0, 3.0)
    plt.ylim(0, 0.0025)
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (A)")
    plt.scatter(l_voltage, l_current, s=5, c='blue')

    plt.show()
    return

volt_increase(device)
