# Marc Serrano Altena
# 06-11-2023
# gets the controller data to use for the experiment
from arduino_device import ArduinoVISADevice, list_devices

device = ArduinoVISADevice(port = "ASRL5::INSTR")

class DiodeExperiment:
    def __init__(self):
        self.resistance = 220 #ohm
        self.voltage_list = []
        self.current_list = []
    
    def scan(self, device, start, stop):
        for output_value in range(start, stop + 1): 
            device.set_output_value(output_value)
            voltage_tot = device.get_input_value_voltage(channel=1)
            voltage_r = device.get_input_value_voltage(channel=2)
            voltage_led = voltage_tot - voltage_r
            current = voltage_r/self.resistance

            self.voltage_list.append(voltage_led)
            self.current_list.append(current)

        # to turn of LED after experiment
        device.set_output_value(0)    