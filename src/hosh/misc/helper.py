#  Copyright (c) 2021. Davi Pereira dos Santos
#  This file is part of the hosh project.
#  Please respect the license - more about this in the section (*) below.
#
#  hosh is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  hosh is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with hosh.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and is unethical regarding the effort and
#  time spent here.
"""Just shortcuts"""
from dataclasses import dataclass

from hosh.hosh_ import Hosh


@dataclass
class Helper:
    """Internal use only.

    Not to be directly instantiated."""

    version: str

    def __call__(self, blob, etype="ordered"):
        return Hosh(blob, etype=etype, version=self.version)

    def u(self, blob):
        return Hosh(blob, etype="unordered", version=self.version)

    def h(self, blob):
        return Hosh(blob, etype="hybrid", version=self.version)

    fromid = Hosh.fromid
    fromn = Hosh.fromn
