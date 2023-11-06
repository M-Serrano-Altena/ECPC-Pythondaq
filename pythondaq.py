import pyvisa
import time
from random import *
import matplotlib.pyplot as plt
import csv

def list_devices():
    rm = pyvisa.ResourceManager("@py")

    return rm.list_resources()

class ArduinoVISADevice:

    def __init__(self, port):
        self.port = port
        self.rm = pyvisa.ResourceManager("@py")
        self.device = self.rm.open_resource(
            "ASRL5::INSTR", read_termination="\r\n", write_termination="\n"
        )

    @staticmethod
    def ADC_to_volt(ADC):
        return round(int(ADC) * 3.3/1023, 2)

    @staticmethod
    def volt_to_ADC(U):
        return int(round(U * 1023/3.3))

    def get_identification(self):
        return self.device.query("*IDN?")

    def set_output_value(self, adc_value):
        # adc_value % 1024 to get values between 0 and 1023
        self.device.query(f"OUT:CH0 {adc_value % 1024}")
        return

    def get_output_value(self):
        return self.device.query("OUT:CH0?")

    def get_input_value(self, channel):
        return int(self.device.query(f"MEAS:CH{channel}?"))
    
    def get_input_value_voltage(self, channel):
        return self.ADC_to_volt(self.device.query(f"MEAS:CH{channel}?"))

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
