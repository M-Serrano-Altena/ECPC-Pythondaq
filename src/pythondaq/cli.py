# Marc Serrano Altena
# 23-11-2023
"""views the data with a command line interface
"""

from pythondaq.diode_experiment import DiodeExperiment, make_connection, list_devices_model
import matplotlib.pyplot as plt
import csv
import click


def view_data(port: str, filename: str, voltage_input_start: float, voltage_input_end: float, repetitions: int, graph: bool):
    """shows the data from the diode experiment in a (I,U) diagram and exports the current and voltage to a csv file

    Args:
        port: port where the arduino device is connected to
        filename: name of the file to export the data as a csv file
        voltage_input_start: the analog start value of the input voltage
        voltage_input_end: the analog end value of the input voltage
        repetitions: the amount of times the experiment should be repeated
        graph: shows a graph if true, doesn't show graph if false
    """    
    diode = DiodeExperiment(port)
    digital_value_start = diode.device.analog_to_digital(voltage_input_start)
    digital_value_end = diode.device.analog_to_digital(voltage_input_end)
    diode.average_value_scan(start=digital_value_start, stop=digital_value_end, measurement_amount=repetitions)
    print(diode.df_measurement)

    # write the I,U data to a csv when given a name
    if filename != None:
        with open(f"{filename}.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["U", "I", "U error", "I error"])
            for voltage, current, voltage_error, current_error  in zip(
                diode.average_voltage_list, diode.average_current_list, diode.error_voltage_list, diode.error_current_list
            ):
                writer.writerow([voltage, current, voltage_error, current_error])
    
    # plot (I, U) diagram of the LED if graph is True
    if graph:
        plt.figure()
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

def port_search(search: str) -> str:
    """searches for the port 

    Args:
        search: search term that tries to find the arduino port
    
    Returns:
        the port found with the search from all available ports
    """
    port_list = list_devices_model()
    if search != None:
        
        for port in port_list:
            if search in port:
                print(port)
                return port
    else:
        print(port_list)


@click.group()
def cmd_group():
    """Input list, info or scan to run the respective function"""
    pass

@cmd_group.command()
@click.option("-s", "--search", default=None, help="makes a search in the available ports")
def list(search: str):
    """prints the available ports

    Args:
        search: search term for the available ports
    """
    port_search(search)
    

@cmd_group.command()
@click.argument("search")
def info(search: str):
    """prints the identification string of the arduino

    Args:
        search: search term to find the port of the arduino device
    """
    port = port_search(search)     
    device = make_connection(port)
    print(device.get_identification())
    return

@cmd_group.command()
@click.argument("search")
@click.option("-s" ,"--voltage_input_start", type=click.FloatRange(0, 3.3), help="start voltage inputted in the arduino", default=0)
@click.option("-e" ,"--voltage_input_end", type=click.FloatRange(0, 3.3), help="end voltage inputted in the arduino", default=3.3)
@click.option(
    "-f",
    "--filename",
    default=None,
    help="the name of the csv data file that is exported",
    show_default=True,    
)
@click.option("-r", "--repetitions", default=10, help="The amount of repetitions to run the experiment")
@click.option("-g", "--graph", is_flag=True, help="shows graph")
def scan(search: str, filename: str, voltage_input_start: float, voltage_input_end: float, repetitions: int, graph: bool):
    """makes a connection with the arduino and runs the view data function

    Args:
        search: search term to find the port of the arduino device
        filename: name of the csv data file
        voltage_input_start: the analog start value of the input voltage
        voltage_input_end: the analog end value of the input voltage
        repetitions: the amount of times the experiment should be repeated
        graph: shows a graph if true, doesn't show graph if false
    """
    port = port_search(search)
    view_data(port, filename, voltage_input_start, voltage_input_end, repetitions, graph)
    return

if __name__ == "__main__":
    cmd_group()
