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
#  part of this work is illegal and unethical regarding the effort and
#  time spent here.
"""Support modules are hidden here to avoid polluting the API"""


def hoshes(iterable):
    """
    Iterator mapping a list of objects to their hoshes.

    >>> from collections import OrderedDict as D
    >>> from hosh import Hosh
    >>> def f(o):
    ...     o.hosh = Hosh(o["a"].encode())
    ...     return o
    >>> lst = map(f, [D(a="a"), D(a="b"), D(a="c")])
    >>> [h.id for h in hoshes(lst)]
    ['cIXBKPediDiOKabeZ6SthD04rnzaquNXaAEhSud4', '9a.VuUhND-A6QgCpIs7lAAkQnQuXwplmiw8308ao', 'SRbk-ZIvvxEJtxP6dHbZP-gQeBGTGCWI8-d3WK3n']
    """
    from operator import attrgetter
    return map(attrgetter("hosh"), iterable)

def ids(iterable):
    """
    Iterator mapping a list of objects to their hosh ids.

    >>> from collections import OrderedDict as D
    >>> from hosh import Hosh
    >>> def f(o):
    ...     o.hosh = Hosh(o["a"].encode())
    ...     return o
    >>> lst = map(f, [D(a="a"), D(a="b"), D(a="c")])
    >>> [h for h in ids(lst)]
    ['cIXBKPediDiOKabeZ6SthD04rnzaquNXaAEhSud4', '9a.VuUhND-A6QgCpIs7lAAkQnQuXwplmiw8308ao', 'SRbk-ZIvvxEJtxP6dHbZP-gQeBGTGCWI8-d3WK3n']
    """
    from operator import attrgetter
    return map(attrgetter("hosh.id"), iterable)
