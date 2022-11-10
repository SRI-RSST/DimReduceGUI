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
from PyQt5 import QtGui

class DisplayWindow(QWidget):
    """"""
    def __init__(self, icon_file):
        """Construct the main window and component widgets."""
        QMainWindow.__init__(self)
        super(DisplayWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon(icon_file))
        self.setWindowTitle("DimReduceGUI")
    # end constructor



# end DisplayWindow