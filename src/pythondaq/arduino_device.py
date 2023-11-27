# Marc Serrano Altena
# 06-11-2023

"""sets the commands to interact with the arduino
"""

import pyvisa
def list_devices() -> tuple:
    """returns the available ports

    Returns:
        tuple: containing the available ports as strings
    """    
    rm = pyvisa.ResourceManager("@py")

    return rm.list_resources()

class ArduinoVISADevice:
    """gives commands to the arduino device
    """    

    def __init__(self, port: str):
        """makes a connection with the arduino device

        Args:
            port: port where the arduino device is connected to
        """        
        self.port = port
        self.rm = pyvisa.ResourceManager("@py")
        self.device = self.rm.open_resource(
            self.port, read_termination="\r\n", write_termination="\n"
        )

    @staticmethod
    def digital_to_analog(digital_value: int) -> float:
        """Converts a digital value to a analog voltage

        Examples:
            >>> ArduinoVISADevice.digital_to_analog(1023)
            3.3
            >>> ArduinoVISADevice.digital_to_analog(800)
            2.58

        Args:
            digital_value: discrete digital value for the voltage

        Returns:
            a continuous analog voltage
        """        
        return round(int(digital_value) * 3.3/1023, 2)

    @staticmethod
    def analog_to_digital(U: float) -> int:
        """Converts an analog voltage to a digital value

        Examples:
            >>> ArduinoVISADevice.analog_to_digital(3.3)
            1023
            >>> ArduinoVISADevice.analog_to_digital(2.01)
            623

        Args:
            U: a continuous analog voltage

        Returns:
            a discrete digital value for the voltage
        """        
        return int(round(U * 1023/3.3))

    def get_identification(self) -> str:
        """gets information about the hardware of the arduino

        Returns:
            information about the hardware of the arduino
        """        
        return self.device.query("*IDN?")

    def set_output_value(self, digital_value: int):
        """sets the output voltage of the arduino in digital values

        Args:
            digital_value: a discrete digital value for the voltage, 0 or a multiple of 1024 is the minimum, a multiple of 1023 is the max value
        """        
        # adc_value % 1024 to get values between 0 and 1023
        self.device.query(f"OUT:CH0 {digital_value % 1024}")
        return

    def get_output_value(self) -> int:
        """returns the output value of channel 0

        Returns:
            output value of channel 0 in digital_values
        """        
        return int(self.device.query("OUT:CH0?"))

    def get_input_value(self, channel: int) -> int:
        """returns the input value of a certain channel in digital values

        Args:
            channel: the channel on the ardiuno to measure

        Returns:
            input value in digital values
        """        
        return int(self.device.query(f"MEAS:CH{channel}?"))
    
    def get_input_value_voltage(self, channel: int) -> float:
        """returns the input value of a certain channel in analog voltage

        Args:
            channel: the channel on the arduino to measure

        Returns:
            input value in analog voltage
        """        
        return self.digital_to_analog(self.device.query(f"MEAS:CH{channel}?"))
