"""Graphical app to run the diode experiment and show results that can be saved
"""

import sys

from pythondaq.diode_experiment import DiodeExperiment, make_connection, list_devices_model
from PySide6 import QtWidgets
from PySide6.QtCore import Slot
import pyqtgraph as pg
import numpy as np

# PyQtGraph global options
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")


class UserInterface(QtWidgets.QMainWindow):
    """Graphical User interface with start & end voltage and the amount of repetitions per experiment
    """

    def __init__(self):
        """initialise values and create start, end, repetitions widgets"""
        super().__init__()
        self.plot_widget = pg.PlotWidget()
        self.port_list = list_devices_model()

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # voeg geneste layouts en widgets toe
        vbox = QtWidgets.QVBoxLayout(central_widget)
        vbox.addWidget(self.plot_widget)

        menu_label = QtWidgets.QLabel("Arduino Port")
        vbox.addWidget(menu_label)

        self.menu_port = QtWidgets.QComboBox()
        for port in self.port_list:
            self.menu_port.addItem(port)

        vbox.addWidget(self.menu_port)

        # buttons
        hbox_buttons = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox_buttons)
        self.start = QtWidgets.QPushButton("Run Experiment")
        hbox_buttons.addWidget(self.start)
        self.save = QtWidgets.QPushButton("Save Data")
        hbox_buttons.addWidget(self.save)
        hbox_values = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox_values)

        # values with labels
        vbox_start = QtWidgets.QVBoxLayout()
        hbox_values.addLayout(vbox_start)

        start_label = QtWidgets.QLabel("Start Voltage of the Experiment")
        vbox_start.addWidget(start_label)

        self.start_value = QtWidgets.QDoubleSpinBox()
        vbox_start.addWidget(self.start_value)

        vbox_end = QtWidgets.QVBoxLayout()
        hbox_values.addLayout(vbox_end)

        end_label = QtWidgets.QLabel("End Voltage of the Experiment")
        vbox_end.addWidget(end_label)

        self.end_value = QtWidgets.QDoubleSpinBox()
        vbox_end.addWidget(self.end_value)

        vbox_reps = QtWidgets.QVBoxLayout()
        hbox_values.addLayout(vbox_reps)

        reps_label = QtWidgets.QLabel("Amount of repetitions to run the scan")
        vbox_reps.addWidget(reps_label)

        self.repetitions = QtWidgets.QSpinBox()
        vbox_reps.addWidget(self.repetitions)

        # set values of start end and repetitions
        self.start_value.setValue(0)
        self.end_value.setValue(3.3)
        self.repetitions.setValue(5)

        # set start and end ranges
        self.start_value.setRange(0, 3.3)
        self.end_value.setRange(0, 3.3)

        

        # Slots and signals
        self.start.clicked.connect(self.view_data)
        self.save.clicked.connect(self.save_data)

        self.start_value.valueChanged.connect(self.range_boundries)
        self.end_value.valueChanged.connect(self.range_boundries)

    @Slot()
    def view_data(self):
        """shows the data from the diode experiment in a (I,U) diagram
        """
        self.plot_widget.clear()
        port = self.menu_port.currentText()
        voltage_input_start = self.start_value.value()
        voltage_input_end = self.end_value.value()
        repetitions = self.repetitions.value()

        diode = DiodeExperiment(port)
        digital_value_start = diode.device.analog_to_digital(voltage_input_start)
        digital_value_end = diode.device.analog_to_digital(voltage_input_end)
        diode.average_value_scan(
            start=digital_value_start,
            stop=digital_value_end,
            measurement_amount=repetitions,
        )
        self.df_measurement = diode.df_measurement

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
    
    @Slot()
    def range_boundries(self):
        """keeps the start voltage the same or smaller than the end voltage
        """        
        self.start_value.setRange(0, self.end_value.value())
        self.end_value.setRange(self.start_value.value(), 3.3)

    @Slot()
    def save_data(self):
        """saves the data in a csv file with a chosen name
        """        
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(filter="CSV files (*.csv)")
        self.df_measurement.to_csv(filename, index=False)
        


def main():
    """opens the graphical user interface
    """    
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
