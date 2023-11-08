# Marc Serrano Altena
# 06-11-2023
# gets the controller data to use for the experiment
from arduino_device import ArduinoVISADevice, list_devices
import numpy as np

# makes a connection to the arduino device
device = ArduinoVISADevice(port = "ASRL5::INSTR")

# tells the arduino how to run the experiment
class DiodeExperiment:
    # sets the initial values of the experiment
    def __init__(self, device):
        self.device = device
        self.resistance = 220 #ohm
        self.voltage_list = []
        self.current_list = []
        self.voltage_measurements = []
        self.current_measurements = []
    
    # increases output of the arduino untill it has the maximum value and puts the voltage and current of the LED in lists
    def scan(self, start, stop):
        for output_value in range(start, stop + 1): 
            self.device.set_output_value(output_value)
            voltage_tot = self.device.get_input_value_voltage(channel=1)
            voltage_r = self.device.get_input_value_voltage(channel=2)
            voltage_led = voltage_tot - voltage_r
            current = voltage_r/self.resistance

            self.voltage_list.append(voltage_led)
            self.current_list.append(current)

        # to turn of LED after experiment
        self.device.set_output_value(0)

    # runs the scan multiple times to get the average values for every output level and the uncertainty of every output level    
    def average_value_scan(self, start, stop):
        for _ in range(0, 10):
            self.scan(self, start, stop)
            self.voltage_measurements.append(self.voltage_list)
            self.current_measurements.append(self.current_list)
        
        # calculate the average value of 10 measurements for every output level
        self.average_voltage_list = [np.mean((volt1, volt2, volt3, volt4, volt5, volt6, volt7, volt8, volt9, volt10)) for volt1, volt2, volt3, volt4, volt5, volt6, volt7, volt8, volt9, volt10 in zip(self.voltage_measurements[0], self.voltage_measurements[1], self.voltage_measurements[2], self.voltage_measurements[3], self.voltage_measurements[4], self.voltage_measurements[5], self.voltage_measurements[6], self.voltage_measurements[7], self.voltage_measurements[8], self.voltage_measurements[9])]
        self.average_current_list = [np.mean((current1, current2, current3, current4, current5, current6, current7, current8, current9, current10)) for current1, current2, current3, current4, current5, current6, current7, current8, current9, current10 in zip(self.current_measurements[0], self.current_measurements[1], self.current_measurements[2], self.current_measurements[3], self.current_measurements[4], self.current_measurements[5], self.current_measurements[6], self.current_measurements[7], self.current_measurements[8], self.current_measurements[9])]
        
        # calculate the standard deviation (error margin) of the 10 measurements for every output level
        self.error_voltage_list = [np.std((volt1, volt2, volt3, volt4, volt5, volt6, volt7, volt8, volt9, volt10)) for volt1, volt2, volt3, volt4, volt5, volt6, volt7, volt8, volt9, volt10 in zip(self.voltage_measurements[0], self.voltage_measurements[1], self.voltage_measurements[2], self.voltage_measurements[3], self.voltage_measurements[4], self.voltage_measurements[5], self.voltage_measurements[6], self.voltage_measurements[7], self.voltage_measurements[8], self.voltage_measurements[9])]
        self.error_current_list = [np.std((current1, current2, current3, current4, current5, current6, current7, current8, current9, current10)) for current1, current2, current3, current4, current5, current6, current7, current8, current9, current10 in zip(self.current_measurements[0], self.current_measurements[1], self.current_measurements[2], self.current_measurements[3], self.current_measurements[4], self.current_measurements[5], self.current_measurements[6], self.current_measurements[7], self.current_measurements[8], self.current_measurements[9])]
    