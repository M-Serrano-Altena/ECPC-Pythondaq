# Marc Serrano Altena
# 06-11-2023
# gets the controller data to use for the experiment
from pythondaq.arduino_device import ArduinoVISADevice #, list_devices
import numpy as np

# tells the arduino how to run the experiment
class DiodeExperiment:
    # sets the initial values of the experiment
    def __init__(self, device):
        self.device = device
        self.resistance = 220  # ohm
        self.voltage_list = []
        self.current_list = []
        self.voltage_measurements = []
        self.current_measurements = []

    # increases output of the arduino untill it has the maximum value and puts the voltage and current of the LED in lists
    def scan(self, start, stop):
        self.voltage_list = []
        self.current_list = []

        for output_value in range(start, stop + 1):
            self.device.set_output_value(output_value)
            voltage_tot = self.device.get_input_value_voltage(channel=1)
            voltage_r = self.device.get_input_value_voltage(channel=2)
            voltage_led = voltage_tot - voltage_r
            current = voltage_r / self.resistance

            self.voltage_list.append(voltage_led)
            self.current_list.append(current)

        # to turn of LED after experiment
        self.device.set_output_value(0)

    # runs the scan multiple times to get the average values for every output level and the uncertainty of every output level
    def average_value_scan(self, start, stop, measurement_amount):
        for _ in range(0, measurement_amount):
            self.scan(start, stop)
            self.voltage_measurements.append(self.voltage_list)
            self.current_measurements.append(self.current_list)

        # calculate the average value of "measurement_amount" measurements for every output level
        self.average_voltage_list =  np.mean(self.voltage_measurements, axis=0)
        self.average_current_list = np.mean(self.current_measurements, axis=0)

        # calculate the standard deviation (error margin) of the 10 measurements for every output level
        self.std_voltage_list = np.std(self.voltage_measurements, axis=0)
        self.std_current_list = np.std(self.current_measurements, axis=0)

        # error of the average is the standard deviation devided by the sqrt of the amount of measurements to get the average
        self.error_voltage_list = [num/np.sqrt(len(self.voltage_measurements)) for num in self.std_voltage_list]
        self.error_current_list = [num/np.sqrt(len(self.current_measurements)) for num in self.std_current_list]