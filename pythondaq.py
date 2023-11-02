import pyvisa
import time
from random import *
import matplotlib.pyplot as plt

rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()

device = rm.open_resource(
    "ASRL5::INSTR", read_termination="\r\n", write_termination="\n"
)

# U0 has the full current
# U1 measures the current passing through the LED and resistor, which is the full current
# U2 measures the current passing through the resistor\

def volt_to_ADC(U):
    return int(round(U * 1023/3.3))

def ADC_to_volt(ADC):
    return round(ADC * 3.3/1023, 2)

# voltage increases till the max intensity
def volt_increase():
    resistance = 220 #ohm
    l_voltage = []
    l_current = []

    # 1023 is de max output, 1024 gives a voltage of 0
    for adc_u in range(0, 1024): 
        device.query(f"OUT:CH0 {adc_u}")
        
        voltage = ADC_to_volt(adc_u)
        current = round(voltage/resistance , 4)

        l_voltage.append(voltage)
        l_current.append(current)

        # print(f"I = {current}, U = {voltage}")
    
    fig = plt.figure()

    plt.xlim(0, 3.5)
    plt.ylim(0, 0.016)
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (A)")
    plt.plot(l_voltage, l_current, 'b-')

    plt.show()
    return

volt_increase()

# to turn of LED after experiment
device.query(f"OUT:CH0 {0}")