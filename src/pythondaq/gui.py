import sys

from pythondaq.diode_experiment import DiodeExperiment, make_connection
from PySide6 import QtWidgets
from PySide6.QtCore import Slot
import pyqtgraph as pg
import numpy as np

# PyQtGraph global options
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")


class UserInterface(QtWidgets.QMainWindow):
    """Graphical User interface

    Args:
        QtWidgets (class): enables a graphical interface
    """

    def __init__(self):
        """initialise values and create start, end, stepsize widgets"""
        super().__init__()
        self.plot_widget = pg.PlotWidget()

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # voeg geneste layouts en widgets toe
        vbox = QtWidgets.QVBoxLayout(central_widget)

        vbox.addWidget(self.plot_widget)

        self.view_data("ASRL6::INSTR", "measurements", 0, 3.3, 2)
        # Slots and signals

    @Slot()
    def view_data(
        self,
        port: str,
        filename: str,
        voltage_input_start: float,
        voltage_input_end: float,
        repetitions: int,
    ):
        """shows the data from the diode experiment in a (I,U) diagram and exports the current and voltage to a csv file

        Args:
            port: port where the arduino device is connected to
            filename: name of the file to export the data as a csv file
            voltage_input_start: start voltage of the input in the arduino
            voltage_input_end: end voltage of the input in the arduino
            repetitions: the amount of times the experiment should be repeated
        """
        diode = DiodeExperiment(port)
        digital_value_start = diode.device.analog_to_digital(voltage_input_start)
        digital_value_end = diode.device.analog_to_digital(voltage_input_end)
        diode.average_value_scan(
            start=digital_value_start,
            stop=digital_value_end,
            measurement_amount=repetitions,
        )
        print(diode.df_measurement)

        # plot (I, U) diagram of the LED
        self.plot_widget.setLabel("bottom", "Voltage (V)")
        self.plot_widget.setLabel("left", "Current (A)")
        self.plot_widget.plot(
            diode.df_measurement["Average Voltage"],
            diode.df_measurement["Average Current"],
            symbol="o",
            symbolSize=5,
            pen=None,
        )

        error_bars = pg.ErrorBarItem(
            x=diode.df_measurement["Average Voltage"],
            y=diode.df_measurement["Average Current"],
            width=2 * diode.df_measurement["Uncertainty Voltage"],
            height=2 * np.array(diode.df_measurement["Uncertainty Current"]),
        )
        self.plot_widget.addItem(error_bars)

        return


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
