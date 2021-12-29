#  Copyright (c) 2021. Davi Pereira dos Santos and Gabriel Dalforno
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


def root(m, k, mod):
    """
    >>> from hosh.misc.math import cellsroot, cellsmul, cellspow
    >>> p = 1099511627689
    >>> a = [356565433747, 1065474654747, 3646565647, 245465626545, 778334555738, 84633966983]
    >>> for k in range(1, 5):
    ...     r = cellsroot(a, k, p)
    ...     a == cellspow(r, k, p)
    True
    True
    True
    True
    """
    if k == 0:  # pragma: no cover
        raise Exception(f"Root index ({k}) must be higher than zero.")
    if k == 1:
        return m
    coef1 = lambda c: (1 if c == 2 else coef1(c - 1) + (c - 1))
    coef2 = lambda c: (0 if c == 2 else coef1(c - 1) + coef2(c - 1))
    divk = pow(k, -1, mod)
    c1 = coef1(k)
    c2 = coef2(k)
    cells = [0, 0, 0, 0, 0, 0]
    cells[1] = (m[1] * divk) % mod
    cells[3] = (m[3] * divk) % mod
    cells[0] = (m[0] * divk) % mod

    cells[4] = ((m[4] - c1 * cells[1] * cells[3]) * divk) % mod
    cells[2] = ((m[2] - c1 * cells[3] * cells[0]) * divk) % mod

    cells[5] = (
        (m[5] - c1 * cells[1] * cells[2] - c1 * cells[4] * cells[0] - c2 * cells[1] * cells[3] * cells[0]) * divk
    ) % mod
    return cells
