#  Copyright (c) 2021. Davi Pereira dos Santos
#  This file is part of the garoupa project.
#  Please respect the license - more about this in the section (*) below.
#
#  garoupa is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  garoupa is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with garoupa.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and is unethical regarding the effort and
#  time spent here.
"""GaROUPa solves the problem of determining the identity of multi-valued objects or sequences of events
(and provide extra modules for group theory)"""

from garoupa.misc.identity import ø
from .groups import UT40_4
from .hosh import Hosh as H
from .misc.helper import Helper

__pdoc__ = {
    "hosh": False,
}

Hosh = H
"""All identifiers are instances of this class"""

ħ = Helper(UT40_4)
"""Shortcut to create 32-digit Hosh objects"""
identity = ø()
"""Shortcut to the 32-digit identity Hosh object"""
ø = identity
"""Shortcut to the 32-digit identity Hosh object"""
