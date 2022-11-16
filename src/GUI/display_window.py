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

import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui

import numpy as np
import matplotlib
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from pandas import read_csv
from pandas.api.types import is_numeric_dtype

try:
    from .windows.mpl_canvas import MplCanvas
    from .windows.navigation_toolbar import NavigationToolbar
    # from .interactive_click import interactive_points
    # from src.GUI.Windows.plot_functions import *
except ImportError:
    from src.GUI.windows.mpl_canvas import MplCanvas
    from src.GUI.windows.navigation_toolbar import NavigationToolbar
    # from src.GUI.Windows.interactive_click import interactive_points
    # from src.GUI.Windows.plot_functions import *

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
        # Set the initial projection value (2d or 3d)
        self.projection = "2d"  # update from radiobutton

        # Create the menubar and define the menu items.
        self.menubar = self.build_menubar()
        # Create the main widget layout
        self.box = self.build_box_layout()
        # Create the main plot widget (creates member variables in method)
        self.build_main_plot()






        # build the layout and add widgets to it
        layout = QGridLayout()
        toolbar = NavigationToolbar(self.main_plot, self)
        layout.addWidget(toolbar, 0, 0, 1, 1)
        #layout.addWidget(self.main_plot, 1, 0, 1, 1)
        layout.addWidget(self.box, 2, 0, 1, 1)
        layout.setMenuBar(self.menubar)
        self.setLayout(layout)
        minsize = self.minimumSizeHint()
        minsize.setHeight(self.minimumSizeHint().height() + 700)
        minsize.setWidth(self.minimumSizeHint().width() + 700)
        self.setFixedSize(minsize)
    # end constructor


    def build_main_plot(self):
        """Create the main plot widget."""
        #setup Matplotlib and initalize plot
        matplotlib.use('Qt5Agg')
        self.plot_data = []
        self.labels = []
        self.main_plot = MplCanvas(
            self, width=10, height=10, dpi=100, projection="3d")
        sc_plot = self.main_plot.axes.scatter3D(
            [], [], [], s=10, alpha=1, depthshade=False)
        self.main_plot.axes.set_position([-0.2, -0.05, 1, 1])
        self.main_plot.axes.set_facecolor("grey")
        self.main_plot.fig.set_facecolor("grey")

        self.original_xlim = sc_plot.axes.get_xlim3d()
        self.original_ylim = sc_plot.axes.get_ylim3d()
        self.original_zlim = sc_plot.axes.get_zlim3d()
        # picked_pt = interactive_points(main_plot, self.projection, self.plot_data, self.labels, self.ch_path, self.feature_file, self.color, self.imageIDs, colordropdown)

        # Connect the window to open when a point is clicked
        # main_plot.fig.canvas.mpl_connect('pick_event', picked_pt)
    # end build_main_plot


    def check_projection(self, dim, plot):
        if dim == "2d":
            self.projection = dim
            self.main_plot.axes.mouse_init()
            self.main_plot.axes.view_init(azim=-90, elev=90)
            self.main_plot.axes.get_zaxis().line.set_linewidth(0)
            self.main_plot.axes.tick_params(axis='z', labelsize=0)
            self.main_plot.draw()
            self.main_plot.axes.disable_mouse_rotation()
        elif dim == "3d":
            self.projection = dim
            self.main_plot.axes.get_zaxis().line.set_linewidth(1)
            self.main_plot.axes.tick_params(axis='z', labelsize=10)
            self.main_plot.draw()
            #rotate left click, zoom right click (disabled) for key mapping
            # see https://matplotlib.org/stable/api/backend_bases_api.html#matplotlib.backend_bases.MouseButton
            self.main_plot.axes.mouse_init(rotate_btn=1, zoom_btn=[])
        if self.feature_file and self.colordropdown.count() > 0 and len(self.plot_data) > 0:
            self.data_filt(self.colordropdown, self.projection, plot, True)

    # end check_projection


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

    def build_box_layout(self, color_dropdown):
        """Create box layout with control and selection widgets."""
        box = QGroupBox()
        boxlayout = QGridLayout()
        selectfile = QPushButton("Select Feature File")
        prevdata = QPushButton("Import Previous Plot Data (.JSON)")
        exportdata = QPushButton("Export Current Plot Data (.JSON)")
        cmap = QPushButton("Legend Colours")
        map_type = QComboBox()
        map_type.addItems(["PCA", "t-SNE", "UMAP", "Sammon"])
        twod = QRadioButton("2D")
        threed = QRadioButton("3D")
        data_columns = QPushButton("Change Plot Data Columns")
        dimensionbox = QGroupBox()
        dimensionboxlayout = QHBoxLayout()
        dimensionboxlayout.addWidget(twod)
        dimensionboxlayout.addWidget(threed)
        dimensionbox.setLayout(dimensionboxlayout)

        boxlayout.addWidget(QLabel("File Options"), 0, 0, 1, 1)
        boxlayout.addWidget(selectfile, 1, 0, 1, 1)
        boxlayout.addWidget(exportdata, 2, 0, 1, 1)
        boxlayout.addWidget(prevdata, 3, 0, 1, 1)
        boxlayout.addWidget(QLabel("Plot Type"), 0, 1, 1, 1)
        boxlayout.addWidget(map_type, 1, 1, 1, 1)
        boxlayout.addWidget(dimensionbox, 2, 1, 1, 1)
        boxlayout.addWidget(data_columns, 3, 1, 1, 1)
        boxlayout.addWidget(cmap, 2, 2, 1, 1)
        boxlayout.addWidget(QLabel("Color By Labels"), 0, 2, 1, 1)
        boxlayout.addWidget(color_dropdown, 1, 2, 1, 1)
        box.setLayout(boxlayout)

        # Connect the actions associated with buttons
        exportdata.clicked.connect(lambda: print("exportdata") ) #save_file(self, map_type.currentText(), colordropdown) if len(self.plot_data) > 0 else errorWindow("Error Dialog","Please Select Feature File. No data is currently displayed"))
        prevdata.clicked.connect(lambda: print("prevdata") ) #import_file(self, map_type, colordropdown, twod, threed))



        # button features and callbacks
        selectfile.clicked.connect(lambda: print("self.loadFeaturefile")) #(self.colordropdown, map_type, True))
        cmap.clicked.connect(lambda: print("legend_colors(self)")) # if len(self.labels)>0 else errorWindow("Error Dialog","Please Select Feature File. No data is currently displayed"))
        twod.toggled.connect(lambda: print("check_projection 2")) #("2d", map_type.currentText()) if twod.isChecked() else None)
        threed.toggled.connect(lambda: print("check_projection 3")) #("3d", map_type.currentText()) if threed.isChecked() else None)
        twod.setChecked(True)
        data_columns.clicked.connect(lambda: print("self.loadFeaturefile")) #(self.colordropdown, map_type, True, prevfile=self.feature_file[0]) if self.feature_file else None)

        self.colordropdown.currentIndexChanged.connect(lambda: self.data_filt(self.colordropdown, self.projection, map_type.currentText(),False) if self.feature_file and self.colordropdown.count() > 0 else None)
        map_type.currentIndexChanged.connect(lambda: self.data_filt(self.colordropdown, self.projection, map_type.currentText(),True) if self.feature_file and self.colordropdown.count() > 0 else None)

        return box
    # end build_box_layout







    def load_feature_file(self, grouping, plot, new_plot, prevfile=None):
        filename=''
        #select feature file button clicked
        if new_plot and isinstance(prevfile, type(None)):
            filename, dump = QFileDialog.getOpenFileName(self, 'Open Feature File', '', "Text files (*.txt *.csv)")
            print(filename, dump)
        #importing or changing data columns
        elif isinstance(prevfile, str) and os.path.exists(prevfile) == False:
            errorWindow("Feature File Error","Feature File Path found in selected Plot Data file does not exist: \n'{}'".format(prevfile))
        if filename != '' or (not isinstance(prevfile, type(None)) and os.path.exists(prevfile)):
            try:
                self.feature_file.clear()
                #new feature file
                if new_plot and filename:
                    self.feature_file.append(filename)
                else:
                    self.feature_file.append(prevfile)
                print(self.feature_file)
                #call selectwindow
                grouping, cancel=self.color_groupings(grouping, plot, new_plot, prevfile)
                if not cancel: #proceed if cancel button not clicked
                    reset_view(self)
                    self.data_filt(grouping, self.projection, plot.currentText(), new_plot)
                    self.numcluster=None
            except Exception as ex:
                if len(self.plot_data)==0:
                    grouping.clear()
                errorWindow("Feature File Error", "Check Validity of Feature File (.txt). \nPython Exception Error: {}".format(traceback.format_exc()))
    # end load_feature_file






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