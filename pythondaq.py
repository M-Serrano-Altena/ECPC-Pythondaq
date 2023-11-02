import pyvisa
import time
from random import *

rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()
print(ports)

device = rm.open_resource(
    "ASRL5::INSTR", read_termination="\r\n", write_termination="\n"
)

# voltage increases till the max intensity
def light():
    # 1023 is de max output, 1024 geeft een spanning van 0
    for num in range(0,1024): device.query(f"OUT:CH0 {num}")
    return

light()