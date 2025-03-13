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
from functools import reduce
from operator import mul, add
from sys import maxsize
from typing import Union

from hosh.config import GLOBAL
from hosh.groups import UT40_4, groups
from hosh.misc.colors import ansi2html, id2ansi, id2rgb
from hosh.misc.core import cells_id_fromblob, cells_fromid, id_fromcells
from hosh.misc.encoding.base777 import b777enc
from hosh.misc.exception import (
    WrongContent,
    DanglingEtype,
    CellValueTooHigh,
    WrongIdentifier,
    ElementTooHigh,
    WrongVersion,
)
from hosh.misc.math import cellsmul, cellsinv, cells2int, int2cells, cellspow, cellsroot
from hosh.theme import HTML, ANSI, BW


class Hosh:
    r"""
    Operable hash.

    Generate a Hosh object from a binary content or a list of 6 ints.

    Usage:

    >>> from hosh import Hosh
    >>> a = Hosh(b"lots of data")
    >>> b = Hosh(b"lots of data 2")
    >>> a.id
    '.-0byLo.CdKjKN6RFTYqBIy30OST3oLyjYPf.6p8'
    >>> b.id
    'SXBse5Ie-yUCa7h7gZiHXGkkKdispqxlc4FnCYit'
    >>> (a * b).id
    'ALiaB9XPu.MoIwwoTPYrxqkGfVpktOgUv0tDB3IB'
    >>> (b * a).id
    'gr9psTs5dYGrCCdgWMAPWM4dDDzktOgUv0tDB3IB'
    >>> a * b * ~b == a
    True
    >>> c = Hosh(b"lots of data 3")
    >>> (a * b) * c == a * (b * c)
    True
    >>> e = Hosh(b"lots of data 4")
    >>> f = Hosh(b"lots of data 5")
    >>> e * f != f * e
    True
    >>> a * b != b * a
    True
    >>> x = Hosh(b"lots of data 6", "hybrid")
    >>> y = Hosh(b"lots of data 7", "hybrid")
    >>> z = Hosh(b"lots of data 8", "unordered")
    >>> x * y == y * x
    True
    >>> x * a != a * x
    True
    >>> x * z == z * x
    True
    >>> a * z == z * a
    True
    >>> from hosh import ø
    >>> print(ø)  # Handy syntax using ø for identity.
    0000000000000000000000000000000000000000
    >>> print(ø * "7ysdf98ys34hg543hdf98ysdf98ysdfysdf98ysd")  # str, bytes or int are converted as id, blob or element rank.
    7ysdf98ys34hg543hdf98ysdf98ysdfysdf98ysd
    >>> print(ø * "7ysdf98ysdf98ysdf98ysdfysdf98ysdasddsa32" * "6gdsf76dfqwe123de8gaf87gaf87gaf87agdfa78")
    94UrdYKjCGQWdd5P.W4xvFJgc9hZpIHlhytqHkaa
    >>> h = ø.u * b"sdff"
    >>> print(h)
    f_9e1a267c8_____________________________
    >>> x.id, (+x).id  # Making an ordered x.
    ('ZN_60eec3e6c7b68087329e16b581401a6bb2b1f', '6BDj3b7Mmj7n-6B8XYaP3akO7400s9FlG4AtcHTp')
    >>> +x * y != y * +x
    True
    >>> ++x == x
    True
    >>> x ** y == +(+x * +y)  # a ** b is a shortcut for +(+a * +b)
    True
    >>> x ** y != y ** x
    True
    >>> (x ** b"1") * (y ** b"2") != (x ** b"2") * (y ** b"1")
    True
    >>> (x ** b"1") * (y ** b"2") == (y ** b"2") * (x ** b"1")
    True
    >>> (x ** y) // y == x
    True
    >>> f + e - x == ø - x + e + f  # Alternative (always unordered, i.e., form an Abelian group) operation
    True
    >>> import pickle
    >>> d = pickle.dumps(x, protocol=5)
    >>> d
    b'\x80\x05\x95j\x00\x00\x00\x00\x00\x00\x00\x8c\x08builtins\x94\x8c\x07getattr\x94\x93\x94\x8c\nhosh.hosh_\x94\x8c\x04Hosh\x94\x93\x94\x8c\x06fromid\x94\x86\x94R\x94\x8c(ZN_60eec3e6c7b68087329e16b581401a6bb2b1f\x94\x85\x94R\x94.'
    >>> pickle.loads(d) == x
    True

    Parameters
    ----------
    content
        Binary content to be hashed, or a list of six integers
    etype
        ordered, hybrid, unordered
        According to the subset of the desired element: Z, H\\Z or G\\H
    version
        Group namedtuple: changes the number of digits and robustness against collisions
        UT32_4 is enough for most usages. It accepts more than 4 billion repetitions of the same operation in a row.
        UT64_4 provides unspeakable limits for operations, please see scientific paper for details.
        UT40_4 is recommended and default, since it is the most compatible with other systems (git, SHA-1, etc)
    """

    _n, _id, _ansi_light, _ansi_dark = None, None, None, None
    _sansi_light, _sansi_dark, _sid, _etype, _rgb_light, _rgb_dark = None, None, None, None, None, None

    _etype_inducer, _bits, _ø = None, None, None
    _rev = None
    components_cache_size = 100

    def __init__(self, content, etype="default:ordered", version=UT40_4):
        self.version = version
        self.p, self.p4, self.p6, self.digits, self.bytes, _, _, _, _, _, _ = version
        self._composition_memo = {}
        if isinstance(content, list):
            if etype != "default:ordered":
                raise DanglingEtype(f"Cannot set etype={etype} when providing cells ({content}).")
            if max(content) >= self.p:
                raise CellValueTooHigh(f"A cell value exceeds the limit for the group: {max(content)} >= {self.p}")
            self.cells = content
        elif isinstance(content, bytes):
            if etype == "default:ordered":
                etype = "ordered"
            self.cells, self._id = cells_id_fromblob(content, etype, self.bytes, self.p)
        else:
            raise WrongContent(
                f"No valid content provided: {content}\n" f"It should be a bytes object to be hashed or a list of ints."
            )

    @property
    def ø(self):
        """Identity element compatible with this Hosh object

        Usage:

        >>> from hosh import Hosh
        >>> (b := Hosh(b"23987rg23")).id
        'J5.uRTue8X4r1xu.JFkPbURVVGvTRPSFLncXdyzj'
        >>> b.etype
        'ordered'
        >>> b.ø.etype
        'unordered'
        >>> b.etype == b.ø.etype_inducer
        True
        >>> b.ø.id
        '0000000000000000000000000000000000000000'
        >>> (b.ø * b"qwer").etype
        'ordered'
        """
        if self._ø is None:
            from hosh import Identity

            self._ø = Identity(version=self.version, etype_inducer=self.etype)
        return self._ø

    @property
    def rev(self):
        """
        Reversed element (warning: this is not the inverse element)

        Element with the internal cells reversed.
        This operation is its own inverse.

        This is useful wherever a unary operation is needed.
        For instance, a function can be represented as a value by its original identifier,
        and can be represented as (an applied) function by its reversed element identifier.

        Not all hoshes are digest-reversible, i.e., at the digit level, due to the intrinsic mismatch between base 64 (i.e., a power of two) representation and the group (prime) order.
        Therefore, we must resort to reversing the cells.
        As an exception, unordered elements do have (most) digits reversed as it has only one internal cell.

        Probabilistically irrelevant corner cases:
            The presence of empty cells (i.e., with zero value) might cause migration from one etype to another.
            The presence of duplicate cells (i.e., with the same value) might make the hosh reverse to itself.
            See examples below.

        Usage:

        >>> from hosh import Hosh, groups
        >>> h = Hosh.fromid("J5.uRTue8X4r1xu.JFkPbURVVGvTRPSFLncXdyzj").rev
        >>> h.id
        'lUz6uu1ZBCJf342R7-qKOOqWJgaf3TDHx2M.CWGT'
        >>> h.rev.rev == h
        True
        >>> h = Hosh.fromid("ab_cabcdefabcdefabcdefabcdefabcdefabcdef")
        >>> h.rev.id
        'Hh_c7201818f76878562c52010943fe4f2a7f3b2'
        >>> h = Hosh.fromid("2_dbe78441d_____________________________")
        >>> h.rev.id
        '2_dbd14487e_____________________________'

        >>> # Limits of subgroup Z.
        >>> Hosh.fromid(groups[40].firstp).id,  Hosh.fromid(groups[40].lastp).id
        ('0_100000000_____________________________', 'f_8afffffff_____________________________')
        >>> Hosh.fromid(groups[40].firstp).rev.id,  Hosh.fromid(groups[40].lastp).rev.id
        ('0_100000000_____________________________', 'f_8afffffff_____________________________')

        >>> # Limits of subgroup H.
        >>> Hosh.fromid(groups[40].firstp4).id, Hosh.fromid(groups[40].lastp4).id
        ('00_1000000000000000000000000000000000000', '.._87c2a630003eec7dffff561b0000004aeffff')
        >>> Hosh.fromid(groups[40].firstp4).rev.id, Hosh.fromid(groups[40].lastp4).rev.id
        ('00_9ed100000015ffffffff00000000000000000', '.._87c2a630003eec7dffff561b0000004aeffff')
        >>> Hosh.fromid(groups[40].firstp4).cells, Hosh.fromid(groups[40].lastp4).cells
        ([0, 0, 0, 0, 1, 0], [0, 0, 1099511627688, 1099511627688, 1099511627688, 1099511627688])
        >>> Hosh.fromid(groups[40].firstp4).rev.cells, Hosh.fromid(groups[40].lastp4).rev.cells
        ([0, 0, 0, 1, 0, 0], [0, 0, 1099511627688, 1099511627688, 1099511627688, 1099511627688])

        >>> # Limits of group G.
        >>> Hosh.fromid(groups[40].firstp6).id, Hosh.fromid(groups[40].lastp6).id
        ('1000000000000000000000000000000000000000', 'g-8KOjCQREq2Vz8VTc30gLMd..vvX6000ov.....')
        >>> Hosh.fromid(groups[40].firstp6).rev.id, Hosh.fromid(groups[40].lastp6).rev.id
        ('00_1000000000000000000000000000000000000', 'g-8KOjCQREq2Vz8VTc30gLMd..vvX6000ov.....')
        >>> Hosh.fromid(groups[40].firstp6).cells, Hosh.fromid(groups[40].lastp6).cells
        ([0, 1, 0, 0, 0, 0], [1099511627688, 1099511627688, 1099511627688, 1099511627688, 1099511627688, 1099511627688])
        >>> Hosh.fromid(groups[40].firstp6).rev.cells, Hosh.fromid(groups[40].lastp6).rev.cells
        ([0, 0, 0, 0, 1, 0], [1099511627688, 1099511627688, 1099511627688, 1099511627688, 1099511627688, 1099511627688])

        >>> # Near limits of group G.
        >>> Hosh.fromn(groups[40].p4+1).id, Hosh.fromn(groups[40].p6 - 2).id
        ('2000000000000000000000000000000000000000', 'f-8KOjCQREq2Vz8VTc30gLMd..vvX6000ov.....')
        >>> Hosh.fromn(groups[40].p4+1).rev.id, Hosh.fromn(groups[40].p6 - 2).rev.id
        ('ihdwjXvMdIj40gZQq-..5Ai0000j-....3000000', '7XoPrombpt9-UXQnse30Cgud..fcZ6000kv.....')
        >>> Hosh.fromn(groups[40].p4+1).cells, Hosh.fromn(groups[40].p6 - 2).cells
        ([0, 1, 0, 0, 0, 1], [1099511627688, 1099511627688, 1099511627688, 1099511627688, 1099511627688, 1099511627687])
        >>> Hosh.fromn(groups[40].p4+1).rev.cells, Hosh.fromn(groups[40].p6 - 2).rev.cells
        ([1, 0, 0, 0, 1, 0], [1099511627687, 1099511627688, 1099511627688, 1099511627688, 1099511627688, 1099511627688])
        """
        if self._rev is None:
            id = self.id
            if self.etype == "ordered":
                self._rev = Hosh(list(reversed(self.cells)))
            elif self.etype == "hybrid":
                self._rev = Hosh(self.cells[:2] + list(reversed(self.cells[2:])))
            elif self.etype == "unordered":
                self._rev = Hosh.fromid(id[:4] + "".join(reversed(id[4:11])) + "_____________________________")
            else:  # pragma: no cover
                raise Exception(f"Unexpected condition. element type: {self.etype}")
        return self._rev

    @property
    def etype(self):
        """
        Type of this element

        Usage:

        >>> from hosh import Hosh
        >>> Hosh.fromn(5).etype
        'unordered'

        Returns
        -------
        'ordered', 'hybrid' or 'unordered'
        """
        if self._etype is None:
            if sum(self.cells[:5]) == 0:
                self._etype = "unordered"
            elif sum(self.cells[:2]) == 0:
                self._etype = "hybrid"
            else:
                self._etype = "ordered"
        return self._etype

    @property
    def etype_inducer(self):
        """
        Type this element uses to coerce an element of undefined type.

        Usage:

        >>> from hosh import ø, Hosh
        >>> ø.etype_inducer
        'ordered'
        >>> ø.h.etype_inducer
        'hybrid'
        >>> ø.u.etype_inducer
        'unordered'
        >>> Hosh(b"12124").etype_inducer
        'ordered'
        >>> Hosh(b"12124", etype="hybrid").etype_inducer
        'hybrid'

        Returns
        -------
        'ordered', 'hybrid', 'unordered'
        """
        if self._etype_inducer is None:
            self._etype_inducer = self.etype
        return self._etype_inducer

    @property
    def id(self):
        """
        Textual representation of this element

        Returns
        -------
        Textual representation
        """
        if self._id is None:
            self._id = id_fromcells(self.cells, self.digits, self.p)
        return self._id

    @classmethod
    def fromid(cls, id):
        """
        Create an element from a textual id.

        Usage:

        >>> a = Hosh.fromid("abcdefabcdefabcdefabcdefabcdefab")
        >>> a.n
        1094566309952642687224764830259410933250743749332933330234
        >>> a.cells
        [748932665, 516513868, 468764361, 3316970622, 2727293743, 316029245]
        >>> a.etype
        'ordered'
        >>> bid = a.id[:2] + "_" + a.id[3:]
        >>> bid
        'ab_defabcdefabcdefabcdefabcdefab'
        >>> b = Hosh.fromid(bid)
        >>> b.id
        'ab_defabcdefabcdefabcdefabcdefab'
        >>> b.n
        59377482839139050825606534576063885287
        >>> b.cells
        [0, 0, 749449200, 1774140626, 3139018916, 292801225]
        >>> b.etype
        'hybrid'
        >>> Hosh.fromid("0000000000000000000000000000000000000000000000000000000000000000") == 0
        True

        Parameters
        ----------
        id

        Parameters
        ----------
        id

        Returns
        -------
        A new Hosh object
        """

        if len(id) not in groups:
            raise WrongIdentifier(f"Wrong identifier length: {len(id)}   id:[{id}]")
        return Hosh(cells_fromid(id, p=groups[len(id)].p), version=groups[len(id)])

    @classmethod
    def fromn(cls, n: int, version=UT40_4):
        """
        Create a Hosh object representing the given int.

        Default 'p' is according to version UT64.4.

        Usage:

        >>> h = Hosh.fromn(7647544756746324134134)
        >>> h.id
        '00_e49c1c505dcd0039e91000000000000000000'

        Parameters
        ----------
        n
        version

        Returns
        -------
        A new Hosh object
        """
        p, order = version.p, version.p6
        if n > order:
            raise ElementTooHigh(f"Element outside allowed range: {n} >= {order}")
        return Hosh(int2cells(n, p), version=version)

    @property
    def n(self):
        """
        Lexicographic rank of this eloement (according to the format adopted in internal integer cells.

        Returns
        -------
        Number
        """
        if self._n is None:
            self._n = cells2int(self.cells, self.p)
        return self._n

    @property
    def sid(self):
        """
        Shorter id (base-777 using up to 2 bytes utf8 per char)

        Usage:

        >>> from hosh import ø
        >>> (ø * b'65e987978g').sid
        'ȟɟìӧДɫŖāöơɟբƢŊþXÊϱՎҲģţՀɄЌ'

        Returns
        -------
        Short utf-8 textual representation
        """
        if self._sid is None:
            self._sid = b777enc(self.n, self.digits * 5 // 8)
        return self._sid

    @property
    def ansi(self):
        r"""
        Colored textual (ANSI) representation of this element

        >>> from hosh import Hosh
        >>> Hosh.fromid("Iaz3L67a2BQv0GifoWOjWale6LYFTGmJJ1ZPfdoP").ansi
        '\x1b[38;5;229m\x1b[1m\x1b[48;5;0mI\x1b[0m\x1b[38;5;228m\x1b[1m\x1b[48;5;0ma\x1b[0m\x1b[38;5;222m\x1b[1m\x1b[48;5;0mz\x1b[0m\x1b[38;5;223m\x1b[1m\x1b[48;5;0m3\x1b[0m\x1b[38;5;228m\x1b[1m\x1b[48;5;0mL\x1b[0m\x1b[38;5;222m\x1b[1m\x1b[48;5;0m6\x1b[0m\x1b[38;5;222m\x1b[1m\x1b[48;5;0m7\x1b[0m\x1b[38;5;223m\x1b[1m\x1b[48;5;0ma\x1b[0m\x1b[38;5;228m\x1b[1m\x1b[48;5;0m2\x1b[0m\x1b[38;5;221m\x1b[1m\x1b[48;5;0mB\x1b[0m\x1b[38;5;216m\x1b[1m\x1b[48;5;0mQ\x1b[0m\x1b[38;5;186m\x1b[1m\x1b[48;5;0mv\x1b[0m\x1b[38;5;222m\x1b[1m\x1b[48;5;0m0\x1b[0m\x1b[38;5;221m\x1b[1m\x1b[48;5;0mG\x1b[0m\x1b[38;5;181m\x1b[1m\x1b[48;5;0mi\x1b[0m\x1b[38;5;194m\x1b[1m\x1b[48;5;0mf\x1b[0m\x1b[38;5;229m\x1b[1m\x1b[48;5;0mo\x1b[0m\x1b[38;5;228m\x1b[1m\x1b[48;5;0mW\x1b[0m\x1b[38;5;222m\x1b[1m\x1b[48;5;0mO\x1b[0m\x1b[38;5;223m\x1b[1m\x1b[48;5;0mj\x1b[0m\x1b[38;5;228m\x1b[1m\x1b[48;5;0mW\x1b[0m\x1b[38;5;222m\x1b[1m\x1b[48;5;0ma\x1b[0m\x1b[38;5;222m\x1b[1m\x1b[48;5;0ml\x1b[0m\x1b[38;5;223m\x1b[1m\x1b[48;5;0me\x1b[0m\x1b[38;5;228m\x1b[1m\x1b[48;5;0m6\x1b[0m\x1b[38;5;221m\x1b[1m\x1b[48;5;0mL\x1b[0m\x1b[38;5;216m\x1b[1m\x1b[48;5;0mY\x1b[0m\x1b[38;5;186m\x1b[1m\x1b[48;5;0mF\x1b[0m\x1b[38;5;222m\x1b[1m\x1b[48;5;0mT\x1b[0m\x1b[38;5;221m\x1b[1m\x1b[48;5;0mG\x1b[0m\x1b[38;5;181m\x1b[1m\x1b[48;5;0mm\x1b[0m\x1b[38;5;194m\x1b[1m\x1b[48;5;0mJ\x1b[0m\x1b[38;5;229m\x1b[1m\x1b[48;5;0mJ\x1b[0m\x1b[38;5;228m\x1b[1m\x1b[48;5;0m1\x1b[0m\x1b[38;5;222m\x1b[1m\x1b[48;5;0mZ\x1b[0m\x1b[38;5;223m\x1b[1m\x1b[48;5;0mP\x1b[0m\x1b[38;5;228m\x1b[1m\x1b[48;5;0mf\x1b[0m\x1b[38;5;222m\x1b[1m\x1b[48;5;0md\x1b[0m\x1b[38;5;222m\x1b[1m\x1b[48;5;0mo\x1b[0m\x1b[38;5;223m\x1b[1m\x1b[48;5;0mP\x1b[0m'

        Returns
        -------
        Textual representation
        """
        if self._ansi_light is None:
            self._ansi_light, self._ansi_dark = id2ansi(self.id)
        return self._ansi_dark if GLOBAL["dark_theme"] else self._ansi_light

    @property
    def idc(self):  # pragma: no cover
        print("'hosh.idc' is deprecated, use 'hosh.ansi' instead")
        return self.ansi

    @property
    def rgb(self):
        """
        Colored textual (RGB) representation of this element

        >>> from hosh import Hosh
        >>> Hosh.fromid("Iaz3L67a2BQv0GifoWOjWale6LYFTGmJJ1ZPfdoP").rgb
        [[6, 28, 104], [255, 255, 184], [255, 255, 141], [255, 220, 155], [255, 233, 172], [255, 250, 139], [255, 218, 144], [254, 223, 150], [255, 229, 187], [255, 255, 127], [255, 206, 98], [242, 176, 123], [212, 201, 138], [237, 216, 120], [252, 198, 115], [234, 193, 174], [229, 253, 204], [255, 255, 184], [255, 255, 141], [255, 220, 155], [255, 233, 172], [255, 250, 139], [255, 218, 144], [254, 223, 150], [255, 229, 187], [255, 255, 127], [255, 206, 98], [242, 176, 123], [212, 201, 138], [237, 216, 120], [252, 198, 115], [234, 193, 174], [229, 253, 204], [255, 255, 184], [255, 255, 141], [255, 220, 155], [255, 233, 172], [255, 250, 139], [255, 218, 144], [254, 223, 150], [255, 229, 187]]
        """
        if self._rgb_light is None:
            self._rgb_light, self._rgb_dark = id2rgb(self.id)
        return self._rgb_dark if GLOBAL["dark_theme"] else self._rgb_light

    @property
    def html(self):
        """
        HTML page containing a colored textual representation of this element

        Returns
        -------
        Textual representation
        """
        return ansi2html(self.ansi)

    @property
    def shtml(self):
        """Short colored html digest"""
        return ansi2html(self.sansi)

    @property
    def sidc(self):  # pragma: no cover
        print("'hosh.sidc' is deprecated, please use 'hosh.sansi' instead")
        return self.sansi

    @property
    def sansi(self):
        """
        Shorter colored id (base-777 using up to 2 bytes utf8 per char)

        Usage:

        >>> from hosh import ø
        >>> print((ø * b'65e987978g').sansi)
        \x1b[38;5;156m\x1b[1m\x1b[48;5;0mȟ\x1b[0m\x1b[38;5;155m\x1b[1m\x1b[48;5;0mɟ\x1b[0m\x1b[38;5;185m\x1b[1m\x1b[48;5;0mì\x1b[0m\x1b[38;5;113m\x1b[1m\x1b[48;5;0mӧ\x1b[0m\x1b[38;5;119m\x1b[1m\x1b[48;5;0mД\x1b[0m\x1b[38;5;185m\x1b[1m\x1b[48;5;0mɫ\x1b[0m\x1b[38;5;113m\x1b[1m\x1b[48;5;0mŖ\x1b[0m\x1b[38;5;119m\x1b[1m\x1b[48;5;0mā\x1b[0m\x1b[38;5;149m\x1b[1m\x1b[48;5;0mö\x1b[0m\x1b[38;5;113m\x1b[1m\x1b[48;5;0mơ\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0mɟ\x1b[0m\x1b[38;5;155m\x1b[1m\x1b[48;5;0mբ\x1b[0m\x1b[38;5;149m\x1b[1m\x1b[48;5;0mƢ\x1b[0m\x1b[38;5;119m\x1b[1m\x1b[48;5;0mŊ\x1b[0m\x1b[38;5;185m\x1b[1m\x1b[48;5;0mþ\x1b[0m\x1b[38;5;119m\x1b[1m\x1b[48;5;0mX\x1b[0m\x1b[38;5;156m\x1b[1m\x1b[48;5;0mÊ\x1b[0m\x1b[38;5;155m\x1b[1m\x1b[48;5;0mϱ\x1b[0m\x1b[38;5;185m\x1b[1m\x1b[48;5;0mՎ\x1b[0m\x1b[38;5;113m\x1b[1m\x1b[48;5;0mҲ\x1b[0m\x1b[38;5;119m\x1b[1m\x1b[48;5;0mģ\x1b[0m\x1b[38;5;185m\x1b[1m\x1b[48;5;0mţ\x1b[0m\x1b[38;5;113m\x1b[1m\x1b[48;5;0mՀ\x1b[0m\x1b[38;5;119m\x1b[1m\x1b[48;5;0mɄ\x1b[0m\x1b[38;5;149m\x1b[1m\x1b[48;5;0mЌ\x1b[0m

        Returns
        -------
        Short utf-8 colored textual representation
        """
        if self._sansi_light is None:
            self._sansi_light, self._sansi_dark = id2ansi(self.sid)
        return self._sansi_dark if GLOBAL["dark_theme"] else self._sansi_light

    def __repr__(self):
        if GLOBAL["format"] == BW:
            return self.sid if GLOBAL["short"] else self.id
        elif GLOBAL["format"] == ANSI:
            return self.sansi if GLOBAL["short"] else self.ansi
        elif GLOBAL["format"] == HTML:
            return self.shtml if GLOBAL["short"] else self.html
        elif callable(GLOBAL["format"]):  # pragma: no cover
            return GLOBAL["format"](self)
        else:  # pragma: no cover
            raise Exception(f"Unknown format: {GLOBAL['format']}")

    def __xor__(self, other: int):
        if other == 1:
            return self
        return Hosh(cellspow(self.cells, other, self.p), version=self.version)

    def __mul__(self, other: Union["Hosh", str, bytes, int]):
        if (other := self.convert(other)) is NotImplemented:  # pragma: no cover
            return NotImplemented
        return Hosh(cellsmul(self.cells, other.cells, self.p), version=self.version)

    def __rmul__(self, other: Union["Hosh", str, bytes, int]):
        """
        >>> from hosh import ø
        >>> (ø * b"13dfv34y4" )* b"434vbfrdg" == b"13dfv34y4" * (ø * b"434vbfrdg")
        True

        Parameters
        ----------
        other

        Returns
        -------

        """
        if (other := self.convert(other)) is NotImplemented:  # pragma: no cover
            return NotImplemented
        return Hosh(cellsmul(other.cells, self.cells, self.p), version=self.version)

    def __rpow__(self, other):
        """
        >>> from hosh import ø
        >>> (ø * b"13dfv34y4") ** b"434vbfrdg" == b"13dfv34y4" ** (ø * b"434vbfrdg")
        True

        Parameters
        ----------
        other

        Returns
        -------

        """
        if (other := self.convert(other)) is NotImplemented:  # pragma: no cover
            return NotImplemented
        return +(+other * +self)

    def __pow__(self, power, modulo=None):
        if (power := self.convert(power)) is NotImplemented:  # pragma: no cover
            return NotImplemented
        return +(+self * +power)

    def __rfloordiv__(self, other):
        """
        >>> from hosh import ø
        >>> (ø * b"13dfv34y4") // b"434vbfrdg" == b"13dfv34y4" // (ø * b"434vbfrdg")
        True

        Parameters
        ----------
        other

        Returns
        -------

        """
        if (other := self.convert(other)) is NotImplemented:  # pragma: no cover
            return NotImplemented
        return +(+other / +self)

    def __floordiv__(self, other):
        """Lift"""
        if (other := self.convert(other)) is NotImplemented:  # pragma: no cover
            return NotImplemented
        return +(+self / +other)

    def __neg__(self):
        return Hosh(cellsinv(self.cells, self.p, additive=True), version=self.version)

    def __pos__(self):
        """Change disposition of element-matrix cells in a way that even hybrid ids will not commute.
        ps. Semantics of +hosh are completely unrelated from -hosh as -hosh creates the inverse additive element.

        Switch positions of cells a2 and a5. This operation is its own inverse.

        Cells are represented as a list in the format: [a5, a4, a3, a2, a1, a0]
        Cells are represented as a matrix in the format:
        1 a4 a1 a0
        0  1 a2 a3
        0  0  1 a5
        0  0  0  1

        """
        cells = self.cells.copy()
        cells[3] = cells[0]
        cells[0] = self.cells[3]
        return Hosh(cells, version=self.version)

    def __invert__(self):
        return Hosh(cellsinv(self.cells, self.p), version=self.version)

    def __rtruediv__(self, other):
        """
        >>> from hosh import ø
        >>> (ø * b"13dfv34y4") / b"434vbfrdg" == b"13dfv34y4" / (ø * b"434vbfrdg")
        True

        Parameters
        ----------
        other

        Returns
        -------

        """
        if (other := self.convert(other)) is NotImplemented:  # pragma: no cover
            return NotImplemented
        return Hosh(cellsmul(other.cells, cellsinv(self.cells, self.p), self.p), version=self.version)

    def __truediv__(self, other):
        if (other := self.convert(other)) is NotImplemented:  # pragma: no cover
            return NotImplemented
        return Hosh(cellsmul(self.cells, cellsinv(other.cells, self.p), self.p), version=self.version)

    def __add__(self, other):
        """Matrix addition modulo p, keeping unidiagonal"""
        if (other := self.convert(other)) is NotImplemented:  # pragma: no cover
            return NotImplemented
        cells = list(map(lambda x, y: (x + y) % self.p, self.cells, other.cells))
        return Hosh(cells, version=self.version)

    def __sub__(self, other):  #TODO: check if a - b  here is different from a + (-b) ?
        """Matrix subtraction modulo p, keeping unidiagonal"""
        if (other := self.convert(other)) is NotImplemented:  # pragma: no cover
            return NotImplemented
        cells = list(map(lambda x, y: (x - y) % self.p, self.cells, other.cells))
        return Hosh(cells, version=self.version)
        # REMINDER: the chosen implementation differs from the alternative bellow!
        # return Hosh.fromn((self.n + self.convert(other).n) % self.order, self.version)

    def __str__(self):
        return self.sid if GLOBAL["short"] else self.id

    def __eq__(self, other):
        if (other := self.convert(other)) is NotImplemented:  # pragma: no cover
            return NotImplemented
        return self.n == other.n

    def __ne__(self, other):
        if (other := self.convert(other)) is NotImplemented:  # pragma: no cover
            return NotImplemented
        return self.n != other.n

    def show(self, colored=True):
        """
        Usage:

        >>> Hosh(b"asdf86fasd").show(colored=False)
        voh8t1KrYmzCqpyrUO9.5QbGdouoZsnExarMSa34
        """
        return print(self.ansi if colored else self.id)

    def short(self, colored=True):
        """
        Usage:

        >>> Hosh(b"asdf86fasd").short(colored=False)
        lϊӑơӫǯÃϺŮϳȐŁЬĽҪƉǏԛȪƜfÞӠȕՇ
        """
        return print(self.sansi if colored else self.sid)

    def __hash__(self):
        return self.n % maxsize

    def convert(self, other):
        """
        Usage:

        >>> from hosh import ø
        >>> ø.convert([0,0,0,0,0,0]).id
        '0000000000000000000000000000000000000000'

        >>> from hosh import Hosh
        >>> ø.convert(0).id
        '0000000000000000000000000000000000000000'

        Parameters
        ----------
        other

        Returns
        -------

        """
        if isinstance(other, str):
            other = Hosh.fromid(other)
        elif isinstance(other, bytes):
            other = Hosh(other, etype=self.etype_inducer, version=self.version)
        elif isinstance(other, int):
            other = Hosh.fromn(other, version=self.version)
        elif isinstance(other, list):
            other = Hosh(other, version=self.version)
        elif not isinstance(other, Hosh):
            return NotImplemented
        if self.version != other.version:
            raise WrongVersion(f"Incompatible operands: {self.version} != {other.version}")
        return other

    def root(self, k):
        """
        >>> a = Hosh(b"a")
        >>> for i in range(1, 5):
        ...     r = a.root(i)
        ...     r^i == a
        True
        True
        True
        True
        """
        if k == 1:
            return self
        return Hosh(cellsroot(self.cells, k, self.p), version=self.version)

    def power_component(self, i, n):
        """Elements corresponding to `n` components of "multiplicative decomposition" such that
        `x  =  x1 * x2 * x3 * ... * xn  =  x * x² * x³ * ... * x^n`

        Not very useful as the resulting elements commute among themselves.
        This happens because they are all powers of x, making up just a sequence of `x`s .

        Parameters
        ==========
        i
            Desired component index
        n
            Desired total number of components

        Returns
        =======
            Hosh (component)

        >>> a = Hosh(b"a")
        >>> a.power_component(0, 1) == a
        True
        >>> a.power_component(0, 2) * a.power_component(1, 2) == a
        True
        >>> a.power_component(0, 3) * a.power_component(1, 3) * a.power_component(2, 3) == a
        True
        >>> a.power_component(2, 3) * a.power_component(1, 3) * a.power_component(0, 3) == a
        True
        """
        if i >= n:  # pragma: no cover
            raise Exception(f"Hosh component should be defined by 'index' ({i}) < '#components' ({n})")
        if n == 1:
            return self
        exp = n * (n + 1) // 2
        r = self.root(exp)
        return r ^ (i + 1)

    def bad_additive_components(self, n):
        """
        Return the `n` additive components for `x` such that `x = x1 + x2 + ... + xn`

        `xn` fills the gap left by the other components remainder.
        We do not recommend this "decomposition" as it always generates different ids for the same subvalue.
        For instance,
            if a list `[value1, value2, value3]` induces ids `a`, `b`, and `any`,
             another list `[value1, value2, ...]` necessarily induces `c` and `d` as first two ids such that `a != c` and `b != d`.

        Parameters
        ==========
        n
            Desired total number of components

        Returns
        =======
            Generator of hoshes

        >>> from functools import reduce
        >>> import operator
        >>> reduce(operator.add, Hosh(b"x").bad_additive_components(5)) == Hosh(b"x")
        True
        """
        den = n * (n + 1) // 2
        p = self.p

        def fac(x):
            parc, rem = divmod(x + p, den)
            lst = [i * parc for i in range(1, n + 1)]
            lst[-1] += rem
            return [l % p for l in lst]

        return (Hosh(list(x), version=self.version) for x in zip(*(fac(c) for c in self.cells)))

    def bad_additive_component(self, i, n):
        """
        Return the `i`-th additive component for `x` such that `x = x1 + x2 + ... + xn`

        See `bad_additive_components` for more details.

        >>> from functools import reduce
        >>> import operator
        >>> list(Hosh(b"x").bad_additive_components(2))[0] == Hosh(b"x").bad_additive_component(0, 2)
        True
        >>> list(Hosh(b"x").bad_additive_components(2))[1] == Hosh(b"x").bad_additive_component(1, 2)
        True
        >>> list(Hosh(b"x").bad_additive_components(3))[0] == Hosh(b"x").bad_additive_component(0, 3)
        True
        >>> list(Hosh(b"x").bad_additive_components(3))[1] == Hosh(b"x").bad_additive_component(1, 3)
        True
        >>> list(Hosh(b"x").bad_additive_components(3))[2] == Hosh(b"x").bad_additive_component(2, 3)
        True
        >>> list(Hosh(b"x").bad_additive_components(5))[0] == Hosh(b"x").bad_additive_component(0, 5)
        True
        >>> list(Hosh(b"x").bad_additive_components(5))[1] == Hosh(b"x").bad_additive_component(1, 5)
        True
        >>> list(Hosh(b"x").bad_additive_components(5))[2] == Hosh(b"x").bad_additive_component(2, 5)
        True
        >>> list(Hosh(b"x").bad_additive_components(5))[4] == Hosh(b"x").bad_additive_component(4, 5)
        True
        >>> list(Hosh(b"x").bad_additive_components(7))[0] == Hosh(b"x").bad_additive_component(0, 7)
        True
        >>> list(Hosh(b"x").bad_additive_components(7))[1] == Hosh(b"x").bad_additive_component(1, 7)
        True
        >>> list(Hosh(b"x").bad_additive_components(7))[2] == Hosh(b"x").bad_additive_component(2, 7)
        True
        >>> list(Hosh(b"x").bad_additive_components(7))[4] == Hosh(b"x").bad_additive_component(4, 7)
        True
        """
        den = n * (n + 1) // 2
        p = self.p
        i += 1
        toggle = 1 if i == n else 0

        def fac(x):
            parc, rem = divmod(x + p, den)
            return (i * parc + toggle * rem) % p

        return Hosh(list(fac(c) for c in self.cells), version=self.version)

    def components(self, start, stop, n, additive=False):
        r"""
        Pseudo"decomposition" based on the hosh of the current id concatenated as bytes to a given component index

        Perform a multiplicative decomposition by default.

        Syntax:
            Hosh(b"blob").components(i, m, n)   # Takes a slice of elements.
            Hosh(b"blob")[i:m, n]               # Takes a slice of elements.
            Hosh(b"blob")[i, n]                 # Takes element `i` out of `n` components.
            Hosh(b"blob")[:n, n]                # All `n` elements.
        Warning:
            Hosh(b"blob")[-1]                   # Reverse element. Not to be confused with inverse element.


        The components are arbitrarily internally defined group elements based on current id as hashed bytes:
        Hosh(id+"-1"), Hosh(id+"-2"), ..., Hosh(id+"-n")

        The last element (xn) is the exception as it makes the product x1 * x2 * ... * xn match x:
        x1      = id+"-1" * x
         ...
        xn-1    = id+"-n-1" * x
        xn      = (id+"-1" * x * ... * id+"-n-1")-¹

        Parameters
        ==========
        start
            Start of a slice
        stop
            Stop of a slice
        n
            Desired total number of components
        additive
            Set up an additive decomposition

        Returns
        =======
            List if hoshes

        >>> from hosh import Hosh
        >>> a = Hosh(b"a")
        >>> a[-1].rev == a
        True
        >>> a[0, 1] == a
        True
        >>> a[0:, 1][0] == a
        True
        >>> a[:1, 1][0] == a
        True
        >>> a[0:1, 1][0] == a
        True
        >>> from operator import mul
        >>> reduce(mul, a[:, 3]) == a
        True
        >>> [x.id for x in a[:, 3]]
        ['Bd6Axil5pFSp15HUBz8eCujvu3gBsEk6XMpRsMNo', '32MloLPcivDbbPMCJn1RBY31aNZ6z-Dqnt4vQhot', 'la3xnZmlhn3lFBAnvWw-UWAvK.2hk-QqUNFYAs3e']
        >>> a[:, 3][0] * a[:, 3][1] * a[:, 3][2] == a
        True
        >>> a[0, 3] * a[1, 3] * a[2, 3] == a
        True
        >>> a.id
        'cIXBKPediDiOKabeZ6SthD04rnzaquNXaAEhSud4'
        >>> from operator import add, mul
        >>> from functools import reduce
        >>> print("\n".join(x.id for x in a.components(0, 7, 7)))
        Bd6Axil5pFSp15HUBz8eCujvu3gBsEk6XMpRsMNo
        32MloLPcivDbbPMCJn1RBY31aNZ6z-Dqnt4vQhot
        Y2JlyuF8.KJc0DvvcIivLA5uLYloF7HN9ovO14Sq
        6.F-NB-G4vBXs7evbBImex9x3foNi85Ca7wDb1c3
        tZmUsjVcZAGTajUOzsSNrr7a7BQVNSiA6xaiPEYf
        iCLMdAlduXvUtK1.awng0D0YP49kV8Cit7OLXyab
        BA6UvITsIN822llT9eErc1R0rmf.ARbc0adwEbWk
        >>> reduce(mul, a.components(0, 2, 7)) * reduce(mul, a.components(2, 3, 7)) * reduce(mul, a.components(3, 7, 7)) == a
        True
        >>> reduce(mul, a.components(0, 7, 7)) == a
        True

        >>> print("\n".join(x.id for x in a.components(0, 7, 7, additive=True)))
        Bd6Axil5pFSp15HUBz8eCujvu3gBsEk6XMpRsMNo
        32MloLPcivDbbPMCJn1RBY31aNZ6z-Dqnt4vQhot
        Y2JlyuF8.KJc0DvvcIivLA5uLYloF7HN9ovO14Sq
        6.F-NB-G4vBXs7evbBImex9x3foNi85Ca7wDb1c3
        tZmUsjVcZAGTajUOzsSNrr7a7BQVNSiA6xaiPEYf
        iCLMdAlduXvUtK1.awng0D0YP49kV8Cit7OLXyab
        7jJmsfrPpa2CeeYCAiByF3HW2J9.ARbc0adwEbWk
        >>> reduce(add, a.components(0, 2, 7, additive=True)) + reduce(add, a.components(2, 3, 7, additive=True)) + reduce(add, a.components(3, 7, 7, additive=True)) == a
        True
        >>> reduce(add, a.components(0, 7, 7, additive=True)) == a
        True
        """
        if stop > n:  # pragma: no cover
            raise Exception(f"Wrong value:   stop=`{stop}`  >=  n=`{n}`")
        acc = self.ø
        operator = add if additive else mul
        for i in range(0, stop):
            if stop == n and i == stop - 1:
                break
            if (t := (i, n, additive)) not in self._composition_memo:
                self._composition_memo[t] = Hosh(f"{self.id}-{i}".encode(), version=self.version)
                if len(self._composition_memo) > self.components_cache_size:  # pragma: no cover
                    first = next(iter(self._composition_memo))
                    del self._composition_memo[first]
            h = self._composition_memo[t]
            acc = operator(acc, h)
            if i >= start:
                yield h
        if stop == n:
            inv = Hosh(cellsinv(acc.cells, self.p, additive), version=self.version)
            last = operator(inv, self)
            yield last

    def __getitem__(self, item: Union[int, tuple]):
        """
        Reverse element:    Hosh(b"blob")[-1]
        """
        if item == -1:
            return self.rev
        if not isinstance(item, tuple) or len(item) != 2:  # pragma: no cover
            raise Exception("Wrong syntax, tuple or `-1` expected: hosh[-1] or hosh[i, n] or hosh[l:m, n]")
        slc, n = item
        if n <= 0:  # pragma: no cover
            raise Exception(f"Wrong value: n={n}  <=  0")

        if isinstance(idx := slc, int):
            if idx < n - 1:
                return Hosh(f"{self.id}-{idx}".encode())
            if n == 1:
                return self
            if idx == n - 1:
                return list(self.components(0, n, n))[idx]
            raise Exception(f"Wrong value: i={slc}  >  n={n}")  # pragma: no cover

        if not isinstance(slc, slice) or slc.step is not None:  # pragma: no cover
            raise Exception(f"Wrong syntax. Simple slice or index expected as first tuple item, not `{slc}`: hosh[i, n] or hosh[l:m, n]")

        if (start := slc.start) is None:
            start = 0
        if (stop := slc.stop) is None:
            stop = n

        if start > n or start < 0:  # pragma: no cover
            raise Exception(f"Wrong values, expected: 0  <=  i={start}  <=  n={n}")
        if n == 1:
            return [self]
        return list(self.components(start, stop, n))

    @property
    def bits(self):
        """
        >>> from hosh import Hosh, groups
        >>> Hosh(b"asd").bits
        '000110111101001001111010010101011100011010000011101010100000000001101101111101100111110100001011001001111001110110101101100110000000011111000110100100110011110010101110100011111101100010010111100111010101010011001110000001000100001101001111'
        >>> bits = Hosh.fromn(groups[40].p6 - 1).bits  # Max number.
        >>> bits
        '111111111111111111111111111111011111011000000000000000000000000110111011011111101111111111111111001101110000101001110100000000000011001100111000100101011110111011111001000010011000001000000100101101100110010011110110001000101011101110110000'
        >>> int(bits, 2) == groups[40].p6 - 1
        True
        """
        if self._bits is None:
            self._bits = '{:b}'.format(self.n).rjust(self.digits * 6, "0")
        return self._bits

    def __reduce__(self):
        return self.fromid, (self.id,)
