# Marc Serrano Altena
# 06-11-2023
# sets the commands to interact with the arduino

import pyvisa
# returns the available ports
def list_devices():
    rm = pyvisa.ResourceManager("@py")

    return rm.list_resources()

# gives commands to the arduino device
class ArduinoVISADevice:

    # makes a connection with the arduino device
    def __init__(self, port):
        self.port = port
        self.rm = pyvisa.ResourceManager("@py")
        self.device = self.rm.open_resource(
            "ASRL5::INSTR", read_termination="\r\n", write_termination="\n"
        )

    # converts an adc value to a voltage
    @staticmethod
    def ADC_to_volt(ADC):
        return round(int(ADC) * 3.3/1023, 2)

    # converts voltage to an adc value
    @staticmethod
    def volt_to_ADC(U):
        return int(round(U * 1023/3.3))

    # gets information about the hardware of the arduino
    def get_identification(self):
        return self.device.query("*IDN?")

    # sets the output voltage of the arduino in adc values
    def set_output_value(self, adc_value):
        # adc_value % 1024 to get values between 0 and 1023
        self.device.query(f"OUT:CH0 {adc_value % 1024}")
        return

    # returns the output value of channel 0 in adc values
    def get_output_value(self):
        return int(self.device.query("OUT:CH0?"))

    # returns the input value of a certain channel in adc values
    def get_input_value(self, channel):
        return int(self.device.query(f"MEAS:CH{channel}?"))
    
    # returns the input value of a certain channel in voltage
    def get_input_value_voltage(self, channel):
        return self.ADC_to_volt(self.device.query(f"MEAS:CH{channel}?"))
