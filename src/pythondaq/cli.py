from pythondaq.view import *
import click


@click.group()
def cmd_group():
    """Input scan or list to run the respective function"""
    pass


@cmd_group.command()
# @click.option(
#     "-n",
#     "--number",
#     default=10,
#     type=int,
#     help="Amount of steps between 0 and 2 pi for the sin function",
#     show_default=True,
# )
def list():
    print("List")
    return


@cmd_group.command()
@click.option("-s" ,"--voltage_input_start", type=click.FloatRange(0, 3.3), help="start voltage inputted in the arduino", default=0)
@click.option("-e" ,"--voltage_input_end", type=click.FloatRange(0, 3.3), help="end voltage inputted in the arduino", default=3.3)
@click.option(
    "-f",
    "--filename",
    default="measurements",
    help="the name of the csv data file that is exported",
    show_default=True,    
)
def scan(filename, voltage_input_start, voltage_input_end):
    main(filename, voltage_input_start, voltage_input_end)
    return


if __name__ == "__main__":
    cmd_group()
