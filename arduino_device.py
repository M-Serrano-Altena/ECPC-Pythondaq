# Marc Serrano Altena
# 06-11-2023
# sets the commands to interact with the arduino

import pyvisa
#
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
        return int(self.device.query("OUT:CH0?"))

    def get_input_value(self, channel):
        return int(self.device.query(f"MEAS:CH{channel}?"))
    
    def get_input_value_voltage(self, channel):
        return self.ADC_to_volt(self.device.query(f"MEAS:CH{channel}?"))
