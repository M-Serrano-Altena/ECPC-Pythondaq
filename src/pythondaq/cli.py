from pythondaq.diode_experiment import *
import matplotlib.pyplot as plt
import csv
import click

# port = ASRL5::INSTR

def view_data(device, filename, voltage_input_start, voltage_input_end, repetitions):
    """shows the data from the diode experiment in a (I,U) diagram and exports the current and voltage to a csv file

    Args:
        device (ArduinoVISADevice): class instance that gives commands to the arduino
        filename (string): name of the file to export the data as a csv file
        voltage_input_start (float): the analog start value of the input voltage
        voltage_input_end (float): the analog end value of the input voltage
        repetition (int): the amount of times the experiment should be repeated
    """    
    diode = DiodeExperiment(device)
    digital_value_start = device.analog_to_digital(voltage_input_start)
    digital_value_end = device.analog_to_digital(voltage_input_end)
    diode.average_value_scan(start=digital_value_start, stop=digital_value_end, measurement_amount=repetitions)
    
    # write the I,U data to a csv
    with open(f"{filename}.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["U", "I", "U error", "I error"])
        for voltage, current, voltage_error, current_error  in zip(
            diode.average_voltage_list, diode.average_current_list, diode.error_voltage_list, diode.error_current_list
        ):
            writer.writerow([voltage, current, voltage_error, current_error])


    # plot (I, U) diagram of the LED
    plt.figure()

    plt.xlim(0, 3.0)
    plt.ylim(0, 0.0025)
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (A)")
    plt.errorbar(
        diode.average_voltage_list,
        diode.average_current_list,
        xerr=diode.error_voltage_list,
        yerr=diode.error_current_list,
        fmt="bo-",
        ecolor="k",
        markersize=3,
    )

    plt.show()
    return


@click.group()
def cmd_group():
    """Input list, info or scan to run the respective function"""
    pass

@cmd_group.command()
def list():
    """prints the available ports
    """    
    print(list_devices())
    return

@cmd_group.command()
@click.argument("port")
def info(port):
    """prints the identification string of the arduino

    Args:
        port (string): port of the arduino device
    """    
    device = make_connection(port)
    print(device.get_identification())
    return

@cmd_group.command()
@click.argument("port")
@click.option("-s" ,"--voltage_input_start", type=click.FloatRange(0, 3.3), help="start voltage inputted in the arduino", default=0)
@click.option("-e" ,"--voltage_input_end", type=click.FloatRange(0, 3.3), help="end voltage inputted in the arduino", default=3.3)
@click.option(
    "-f",
    "--filename",
    default="measurements",
    help="the name of the csv data file that is exported",
    show_default=True,    
)
@click.option("-r", "--repetitions", default=10, help="The amount of repetitions to run the experiment")
def scan(port, filename, voltage_input_start, voltage_input_end, repetitions):
    """makes a connection with the arduino and runs the view data function

    Args:
        port (string): port of the arduino device
        filename (string): name of the csv data file
        voltage_input_start (float): the analog start value of the input voltage
        voltage_input_end (float): the analog end value of the input voltage
        repetitions (int): the amount of times the experiment should be repeated
    """    
    device = make_connection(arduino_port=port)
    view_data(device, filename, voltage_input_start, voltage_input_end, repetitions)
    return

if __name__ == "__main__":
    cmd_group()
