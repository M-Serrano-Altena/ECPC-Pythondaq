import pyvisa
import time
from random import *

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
    # 1023 is de max output, 1024 geeft een spanning van 0
    for adc_v in range(0, 1024): 
        device.query(f"OUT:CH0 {adc_v}")
        adc_r = int(device.query(f"MEAS:CH2?"))
        print(f"On LED: {adc_v} ({ADC_to_volt(adc_v)} V)       Over resistor: {adc_r} ({ADC_to_volt(adc_r)} V)")
    
    return

volt_increase()
# to turn of LED after experiment
device.query(f"OUT:CH0 {0}")