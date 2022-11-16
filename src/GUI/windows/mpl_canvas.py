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

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

class MplCanvas(FigureCanvasQTAgg):
    """matplotlib figure-plot creation."""
    def __init__(self, parent=None, width=5, height=5, dpi=100, projection="3d"):
        """Figure plot constructor."""
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        if projection == "3d":
            self.axes = self.fig.add_subplot(111, projection=projection)
        else:
            self.axes = self.fig.add_subplot(111, projection=None)
        super(MplCanvas, self).__init__(self.fig)
        self.cmap = None
    # end constructor

    def set_near_full(self):
        """Set the size of the plot within the containing widget."""
        self.axes.set_aspect('auto')
        self.axes.set_position([0.01, 0.01, 0.98, 0.98])
    # set_near_full
