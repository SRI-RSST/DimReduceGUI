# Copyright (C) 2022 Sunnybrook Research Institute
# This file is part of DimReduceGUI <https://github.com/SRI-RSST/DimReduceGUI>.
#
# DimReduceGUI is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DimReduceGUI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DimReduceGUI.  If not, see <http://www.gnu.org/licenses/>.

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui

import numpy as np
import matplotlib
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from pandas import read_csv
from pandas.api.types import is_numeric_dtype

# try:
#     from .interactive_click import interactive_points
#     from src.GUI.Windows.plot_functions import *
# except ImportError:
#     from src.GUI.Windows.interactive_click import interactive_points
#     from src.GUI.Windows.plot_functions import *

class DisplayWindow(QWidget):
    """"""
    def __init__(self, icon_file):
        """Construct the main window and component widgets."""
        QMainWindow.__init__(self)
        super(DisplayWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon(icon_file))
        self.setWindowTitle("DimReduceGUI")
        self.feature_file = []
        self.imageIDs = []
        self.plots = []
        self.filtered_data = 0
        self.ch_path = []
        self.plotcols = []
        self.raw_col = []
        self.numcluster = None
        self.color = [(0, 0.45, 0.74), (0.85, 0.33, 0.1), (0.93, 0.69, 0.13)]

        # Create the menubar and define the menu items.
        self.menubar = self.build_menubar()






        # build the layout and add widgets to it
        layout = QGridLayout()
        #toolbar = NavigationToolbar(self.main_plot, self)
        #layout.addWidget(toolbar, 0, 0, 1, 1)
        #layout.addWidget(self.main_plot, 1, 0, 1, 1)
        #layout.addWidget(box, 2, 0, 1, 1)
        layout.setMenuBar(self.menubar)
        self.setLayout(layout)
        minsize = self.minimumSizeHint()
        minsize.setHeight(self.minimumSizeHint().height() + 700)
        minsize.setWidth(self.minimumSizeHint().width() + 700)
        self.setFixedSize(minsize)
    # end constructor


    def build_menubar(self):
        """Create the menubar and define the menu item actions."""
        the_menubar = QMenuBar()
        file = the_menubar.addMenu("File")
        inputfile = file.addAction("Select Feature File")
        data = the_menubar.addMenu("Data Analysis")
        clustering = data.addMenu("Clustering")
        estimate = clustering.addAction("Estimate Clusters")
        setnumber = clustering.addAction("Set Number of Clusters")
        piemaps = clustering.addAction(
            "Cluster Pie Maps (2D - X and Y axis display)")
        export = clustering.addAction("Export Cluster Results")
        plot_properties = the_menubar.addMenu("Plot Properties")
        rotation_enable = plot_properties.addAction(
            "Enable 3D Rotation (Left-Click and Drag)")
        rotation_disable = plot_properties.addAction("Disable 3D Rotation")
        reset_view = plot_properties.addAction("Reset Plot View")

        # Connect the actions associated with each menu item
        inputfile.triggered.connect(
            lambda: print("self.loadFeaturefile(colordropdown, map_type, True)"))
        estimate.triggered.connect(
            lambda: print("Clustering().cluster_est(self.filtered_data)") ) # if len(self.plot_data) > 0 else errorWindow("Error Dialog","Please Select Feature File. No data is currently displayed"))
        setnumber.triggered.connect(lambda: print("self.setnumcluster(colordropdown.currentText())")) # if len(self.plot_data) > 0 else errorWindow("Error Dialog","Please Select Feature File. No data is currently displayed"))
        piemaps.triggered.connect(lambda: print("piechart") ) #(self.plot_data, self.filtered_data, self.numcluster, np.array(self.labels), self.plots[0].get_cmap()) if len(self.plot_data) > 0 else errorWindow("Error Dialog","Please Select Feature File. No data is currently displayed"))
        export.triggered.connect(lambda: print("export_cluster")) #(self.plot_data, self.filtered_data, self.numcluster, self.feature_file[0]) if len(self.plot_data) >0 else errorWindow("Error Dialog","Please Select Feature File. No data is currently displayed"))
        rotation_enable.triggered.connect(lambda: print("self.main_plot.axes.mouse_init(rotate_btn=1, zoom_btn=[])"))
        rotation_disable.triggered.connect(lambda: print("self.main_plot.axes.disable_mouse_rotation()"))
        reset_view.triggered.connect(lambda: print("reset_view(self)"))

        return the_menubar
    # end build_menubar


    # part of box
    #    exportdata.clicked.connect(lambda: save_file(self, map_type.currentText(), colordropdown) if len(self.plot_data) > 0 else errorWindow("Error Dialog","Please Select Feature File. No data is currently displayed"))
    #    prevdata.clicked.connect(lambda: import_file(self, map_type, colordropdown, twod, threed))




    def set_num_cluster(self, group):
        """Build and open the set cluster window, and set the member variable."""
        # clustnum = setcluster(
        #     self.numcluster, self.filtered_data, self.plot_data,
        #     np.array(self.labels), group)
        clustnum = 1
        self.numcluster = clustnum #.clust
    # end set_num_cluster

    def close_event(self, event):
        """Close all windows of the application."""
        for window in QApplication.topLevelWidgets():
            window.close()
    # end close_event
# end DisplayWindow