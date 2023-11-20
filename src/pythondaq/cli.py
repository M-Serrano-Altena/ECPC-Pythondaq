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
def scan():
    print("Scan")
    return

if __name__ == "__main__":
    cmd_group()