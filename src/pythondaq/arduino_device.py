# Marc Serrano Altena
# 06-11-2023
# sets the commands to interact with the arduino

import pyvisa
def list_devices():
    """returns the available ports

    Returns:
        tuple: containing the available ports as strings
    """    
    rm = pyvisa.ResourceManager("@py")

    return rm.list_resources()

class ArduinoVISADevice:
    """gives commands to the arduino device
    """    

    def __init__(self, port):
        """makes a connection with the arduino device

        Args:
            port (string): port where the arduino device is connected to
        """        
        self.port = port
        self.rm = pyvisa.ResourceManager("@py")
        self.device = self.rm.open_resource(
            self.port, read_termination="\r\n", write_termination="\n"
        )

    @staticmethod
    def digital_to_analog(digital_value):
        """Converts a digital value to a analog voltage

        Args:
            digital_value (int): discrete digital value for the voltage

        Returns:
            float: a continuous analog voltage
        """        
        return round(int(digital_value) * 3.3/1023, 2)

    @staticmethod
    def analog_to_digital(U):
        """Converts an analog voltage to a digital value

        Args:
            U (float): a continuous analog voltage

        Returns:
            int: a discrete digital value for the voltage
        """        
        return int(round(U * 1023/3.3))

    def get_identification(self):
        """gets information about the hardware of the arduino

        Returns:
            string: information about the hardware of the arduino
        """        
        return self.device.query("*IDN?")

    def set_output_value(self, digital_value):
        """sets the output voltage of the arduino in digital values

        Args:
            digital_value (int): a discrete digital value for the voltage, 0 or a multiple of 1024 is the minimum, a multiple of 1023 is the max value
        """        
        # adc_value % 1024 to get values between 0 and 1023
        self.device.query(f"OUT:CH0 {digital_value % 1024}")
        return

    def get_output_value(self):
        """returns the output value of channel 0

        Returns:
            int: output value of channel 0 in digital_values
        """        
        return int(self.device.query("OUT:CH0?"))

    def get_input_value(self, channel):
        """returns the input value of a certain channel in digital values

        Args:
            channel (int): the channel on the ardiuno to measure

        Returns:
            int: input value in digital values
        """        
        return int(self.device.query(f"MEAS:CH{channel}?"))
    
    def get_input_value_voltage(self, channel):
        """returns the input value of a certain channel in analog voltage

        Args:
            channel (int): the channel on the arduino to measure

        Returns:
            float: input value in analog voltage
        """        
        return self.digital_to_analog(self.device.query(f"MEAS:CH{channel}?"))
