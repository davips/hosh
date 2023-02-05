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
from typing import Union

from hosh._internals_appearance import ANSI, BW, HTML

GLOBAL = {"dark_theme": True, "format": ANSI(), "short": False}


def setup(dark_theme: bool = None, format: Union[BW, ANSI, HTML, callable] = None, short: bool = None):
    """
    Change global settings

    >>> from hosh import Hosh
    >>> from hosh.config import setup
    >>> from hosh.theme import BW, ANSI, HTML
    >>> Hosh(b"asd")
    \x1b[38;5;71m\x1b[1m\x1b[48;5;0mL\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0ms\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mx\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0mC\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0ma\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0mj\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0ml\x1b[0m\x1b[38;5;78m\x1b[1m\x1b[48;5;0mK\x1b[0m\x1b[38;5;119m\x1b[1m\x1b[48;5;0m8\x1b[0m\x1b[38;5;113m\x1b[1m\x1b[48;5;0m3\x1b[0m\x1b[38;5;113m\x1b[1m\x1b[48;5;0m0\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mA\x1b[0m\x1b[38;5;72m\x1b[1m\x1b[48;5;0mK\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0mq\x1b[0m\x1b[38;5;149m\x1b[1m\x1b[48;5;0mt\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mU\x1b[0m\x1b[38;5;71m\x1b[1m\x1b[48;5;0m5\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0mv\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0m0\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0mC\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0m9\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0mY\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mV\x1b[0m\x1b[38;5;78m\x1b[1m\x1b[48;5;0m9\x1b[0m\x1b[38;5;119m\x1b[1m\x1b[48;5;0mb\x1b[0m\x1b[38;5;113m\x1b[1m\x1b[48;5;0mQ\x1b[0m\x1b[38;5;113m\x1b[1m\x1b[48;5;0mn\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mZ\x1b[0m\x1b[38;5;72m\x1b[1m\x1b[48;5;0mJ\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0m1\x1b[0m\x1b[38;5;149m\x1b[1m\x1b[48;5;0mw\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mG\x1b[0m\x1b[38;5;71m\x1b[1m\x1b[48;5;0m3\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0mq\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0ms\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0ml\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mW\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0m9\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mZ\x1b[0m\x1b[38;5;78m\x1b[1m\x1b[48;5;0m6\x1b[0m

    >>> setup(dark_theme=False)
    >>> Hosh(b"asd")
    \x1b[38;5;2m\x1b[1m\x1b[48;5;15mL\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15ms\x1b[0m\x1b[38;5;22m\x1b[1m\x1b[48;5;15mx\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15mC\x1b[0m\x1b[38;5;22m\x1b[1m\x1b[48;5;15ma\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15mj\x1b[0m\x1b[38;5;22m\x1b[1m\x1b[48;5;15ml\x1b[0m\x1b[38;5;28m\x1b[1m\x1b[48;5;15mK\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15m8\x1b[0m\x1b[38;5;64m\x1b[1m\x1b[48;5;15m3\x1b[0m\x1b[38;5;70m\x1b[1m\x1b[48;5;15m0\x1b[0m\x1b[38;5;64m\x1b[1m\x1b[48;5;15mA\x1b[0m\x1b[38;5;23m\x1b[1m\x1b[48;5;15mK\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15mq\x1b[0m\x1b[38;5;70m\x1b[1m\x1b[48;5;15mt\x1b[0m\x1b[38;5;58m\x1b[1m\x1b[48;5;15mU\x1b[0m\x1b[38;5;2m\x1b[1m\x1b[48;5;15m5\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15mv\x1b[0m\x1b[38;5;22m\x1b[1m\x1b[48;5;15m0\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15mC\x1b[0m\x1b[38;5;22m\x1b[1m\x1b[48;5;15m9\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15mY\x1b[0m\x1b[38;5;22m\x1b[1m\x1b[48;5;15mV\x1b[0m\x1b[38;5;28m\x1b[1m\x1b[48;5;15m9\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15mb\x1b[0m\x1b[38;5;64m\x1b[1m\x1b[48;5;15mQ\x1b[0m\x1b[38;5;70m\x1b[1m\x1b[48;5;15mn\x1b[0m\x1b[38;5;64m\x1b[1m\x1b[48;5;15mZ\x1b[0m\x1b[38;5;23m\x1b[1m\x1b[48;5;15mJ\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15m1\x1b[0m\x1b[38;5;70m\x1b[1m\x1b[48;5;15mw\x1b[0m\x1b[38;5;58m\x1b[1m\x1b[48;5;15mG\x1b[0m\x1b[38;5;2m\x1b[1m\x1b[48;5;15m3\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15mq\x1b[0m\x1b[38;5;22m\x1b[1m\x1b[48;5;15ms\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15ml\x1b[0m\x1b[38;5;22m\x1b[1m\x1b[48;5;15mW\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15m9\x1b[0m\x1b[38;5;22m\x1b[1m\x1b[48;5;15mZ\x1b[0m\x1b[38;5;28m\x1b[1m\x1b[48;5;15m6\x1b[0m

    >>> setup(short=True)
    >>> Hosh(b"asd")
    \x1b[38;5;23m\x1b[1m\x1b[48;5;15mÓ\x1b[0m\x1b[38;5;36m\x1b[1m\x1b[48;5;15mӭ\x1b[0m\x1b[38;5;23m\x1b[1m\x1b[48;5;15mϳ\x1b[0m\x1b[38;5;28m\x1b[1m\x1b[48;5;15mơ\x1b[0m\x1b[38;5;23m\x1b[1m\x1b[48;5;15mӨ\x1b[0m\x1b[38;5;35m\x1b[1m\x1b[48;5;15mǹ\x1b[0m\x1b[38;5;23m\x1b[1m\x1b[48;5;15mƹ\x1b[0m\x1b[38;5;29m\x1b[1m\x1b[48;5;15mO\x1b[0m\x1b[38;5;30m\x1b[1m\x1b[48;5;15mä\x1b[0m\x1b[38;5;2m\x1b[1m\x1b[48;5;15mĎ\x1b[0m\x1b[38;5;23m\x1b[1m\x1b[48;5;15më\x1b[0m\x1b[38;5;29m\x1b[1m\x1b[48;5;15mϊ\x1b[0m\x1b[38;5;28m\x1b[1m\x1b[48;5;15mɜ\x1b[0m\x1b[38;5;23m\x1b[1m\x1b[48;5;15mā\x1b[0m\x1b[38;5;36m\x1b[1m\x1b[48;5;15mҙ\x1b[0m\x1b[38;5;2m\x1b[1m\x1b[48;5;15mĉ\x1b[0m\x1b[38;5;23m\x1b[1m\x1b[48;5;15mý\x1b[0m\x1b[38;5;36m\x1b[1m\x1b[48;5;15mŮ\x1b[0m\x1b[38;5;23m\x1b[1m\x1b[48;5;15mƵ\x1b[0m\x1b[38;5;28m\x1b[1m\x1b[48;5;15mŖ\x1b[0m\x1b[38;5;23m\x1b[1m\x1b[48;5;15mĠ\x1b[0m\x1b[38;5;35m\x1b[1m\x1b[48;5;15mí\x1b[0m\x1b[38;5;23m\x1b[1m\x1b[48;5;15mҺ\x1b[0m\x1b[38;5;29m\x1b[1m\x1b[48;5;15mӞ\x1b[0m\x1b[38;5;30m\x1b[1m\x1b[48;5;15mÀ\x1b[0m

    >>> setup(format=BW, short=False)
    >>> Hosh(b"asd")
    LsxCajlK830AKqtU5v0C9YV9bQnZJ1wG3qslW9Z6

    >>> setup(format=HTML, short=True)
    >>> Hosh(b"asd")
    <style type="text/css">
     .ansi2html-content { display: inline; white-space: pre-wrap; word-wrap: break-word; }
    .body_foreground { color: #000000; }
    .body_background { background-color: #AAAAAA; }
    .inv_foreground { color: #AAAAAA; }
    .inv_background { background-color: #000000; }
    .ansi1 { font-weight: bold; }
    .ansi38-2 { color: #00aa00; }
    .ansi48-15 { background-color: #ffffff; }
    .ansi38-23 { color: #005f5f; }
    .ansi38-28 { color: #008700; }
    .ansi38-29 { color: #00875f; }
    .ansi38-30 { color: #008787; }
    .ansi38-35 { color: #00af5f; }
    .ansi38-36 { color: #00af87; }
    </style>
    <pre class="ansi2html-content"><span class="ansi38-23"></span><span class="ansi1 ansi38-23"></span><span class="ansi1 ansi38-23 ansi48-15">Ó</span><span class="ansi38-36"></span><span class="ansi1 ansi38-36"></span><span class="ansi1 ansi38-36 ansi48-15">ӭ</span><span class="ansi38-23"></span><span class="ansi1 ansi38-23"></span><span class="ansi1 ansi38-23 ansi48-15">ϳ</span><span class="ansi38-28"></span><span class="ansi1 ansi38-28"></span><span class="ansi1 ansi38-28 ansi48-15">ơ</span><span class="ansi38-23"></span><span class="ansi1 ansi38-23"></span><span class="ansi1 ansi38-23 ansi48-15">Ө</span><span class="ansi38-35"></span><span class="ansi1 ansi38-35"></span><span class="ansi1 ansi38-35 ansi48-15">ǹ</span><span class="ansi38-23"></span><span class="ansi1 ansi38-23"></span><span class="ansi1 ansi38-23 ansi48-15">ƹ</span><span class="ansi38-29"></span><span class="ansi1 ansi38-29"></span><span class="ansi1 ansi38-29 ansi48-15">O</span><span class="ansi38-30"></span><span class="ansi1 ansi38-30"></span><span class="ansi1 ansi38-30 ansi48-15">ä</span><span class="ansi38-2"></span><span class="ansi1 ansi38-2"></span><span class="ansi1 ansi38-2 ansi48-15">Ď</span><span class="ansi38-23"></span><span class="ansi1 ansi38-23"></span><span class="ansi1 ansi38-23 ansi48-15">ë</span><span class="ansi38-29"></span><span class="ansi1 ansi38-29"></span><span class="ansi1 ansi38-29 ansi48-15">ϊ</span><span class="ansi38-28"></span><span class="ansi1 ansi38-28"></span><span class="ansi1 ansi38-28 ansi48-15">ɜ</span><span class="ansi38-23"></span><span class="ansi1 ansi38-23"></span><span class="ansi1 ansi38-23 ansi48-15">ā</span><span class="ansi38-36"></span><span class="ansi1 ansi38-36"></span><span class="ansi1 ansi38-36 ansi48-15">ҙ</span><span class="ansi38-2"></span><span class="ansi1 ansi38-2"></span><span class="ansi1 ansi38-2 ansi48-15">ĉ</span><span class="ansi38-23"></span><span class="ansi1 ansi38-23"></span><span class="ansi1 ansi38-23 ansi48-15">ý</span><span class="ansi38-36"></span><span class="ansi1 ansi38-36"></span><span class="ansi1 ansi38-36 ansi48-15">Ů</span><span class="ansi38-23"></span><span class="ansi1 ansi38-23"></span><span class="ansi1 ansi38-23 ansi48-15">Ƶ</span><span class="ansi38-28"></span><span class="ansi1 ansi38-28"></span><span class="ansi1 ansi38-28 ansi48-15">Ŗ</span><span class="ansi38-23"></span><span class="ansi1 ansi38-23"></span><span class="ansi1 ansi38-23 ansi48-15">Ġ</span><span class="ansi38-35"></span><span class="ansi1 ansi38-35"></span><span class="ansi1 ansi38-35 ansi48-15">í</span><span class="ansi38-23"></span><span class="ansi1 ansi38-23"></span><span class="ansi1 ansi38-23 ansi48-15">Һ</span><span class="ansi38-29"></span><span class="ansi1 ansi38-29"></span><span class="ansi1 ansi38-29 ansi48-15">Ӟ</span><span class="ansi38-30"></span><span class="ansi1 ansi38-30"></span><span class="ansi1 ansi38-30 ansi48-15">À</span></pre>

    >>> setup(dark_theme=True, format=ANSI, short=False)


    Parameters
    ----------
    dark_theme
        Black or white background.
    format
        Plain text (BW); coclored text (ANSI); or, colored text for the web (HTML)
    short
        True: base-777; False: base-64
    """
    if dark_theme is not None:
        GLOBAL["dark_theme"] = dark_theme
    if format is not None:
        GLOBAL["format"] = format
    if short is not None:
        GLOBAL["short"] = short
