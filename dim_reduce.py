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

"""Some information about the dimensionality reduction GUI.

Some more details
"""

from os import path
import sys

from PyQt5.QtWidgets import QApplication

from src.GUI.display_window import DisplayWindow

def run_display_window(icon_file):
    """Create an instance of the display window GUI and run the application."""
    app = QApplication(sys.argv)
    window = DisplayWindow(icon_file)
    window.show()
    app.exec()
# end run_display_window

if __name__ == '__main__':
    icon_file = path.abspath(
        path.join(path.dirname(__file__), 'dim_reduce_icon.png'))
    # Start the GUI defined in src/GUI/display_window.py
    run_display_window(icon_file)

# end main