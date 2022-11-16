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

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class NavigationToolbar(NavigationToolbar):
    """Import matplotlib toolbar. Only use desired functions."""
    NavigationToolbar.toolitems = (
        (None, None, None, None),
        (None, None, None, None),
        (None, None, None, None),
        (None, None, None, None),
        (None, None, None, None),
        ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
        (None, None, None, None),
        (None, None, None, None),
        ('Save', 'Save the figure', 'filesave', 'save_figure')
    )
# end NavigationToolbar
