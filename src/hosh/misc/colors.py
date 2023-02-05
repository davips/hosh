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
"""Functions to colorize representation of Hosh objects, e.g. on ipython"""
from hashlib import md5

import colored
from ansi2html import Ansi2HTMLConverter
from colored import stylize

from hosh.config import GLOBAL

from bs4 import BeautifulSoup


def paint(txt, fgr, fgg, fgb, dark):
    """
    >>> from hosh import setup, ø
    >>> ø * b"asd"
    \x1b[38;5;71m\x1b[1m\x1b[48;5;0mL\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0ms\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mx\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0mC\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0ma\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0mj\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0ml\x1b[0m\x1b[38;5;78m\x1b[1m\x1b[48;5;0mK\x1b[0m\x1b[38;5;119m\x1b[1m\x1b[48;5;0m8\x1b[0m\x1b[38;5;113m\x1b[1m\x1b[48;5;0m3\x1b[0m\x1b[38;5;113m\x1b[1m\x1b[48;5;0m0\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mA\x1b[0m\x1b[38;5;72m\x1b[1m\x1b[48;5;0mK\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0mq\x1b[0m\x1b[38;5;149m\x1b[1m\x1b[48;5;0mt\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mU\x1b[0m\x1b[38;5;71m\x1b[1m\x1b[48;5;0m5\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0mv\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0m0\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0mC\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0m9\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0mY\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mV\x1b[0m\x1b[38;5;78m\x1b[1m\x1b[48;5;0m9\x1b[0m\x1b[38;5;119m\x1b[1m\x1b[48;5;0mb\x1b[0m\x1b[38;5;113m\x1b[1m\x1b[48;5;0mQ\x1b[0m\x1b[38;5;113m\x1b[1m\x1b[48;5;0mn\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mZ\x1b[0m\x1b[38;5;72m\x1b[1m\x1b[48;5;0mJ\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0m1\x1b[0m\x1b[38;5;149m\x1b[1m\x1b[48;5;0mw\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mG\x1b[0m\x1b[38;5;71m\x1b[1m\x1b[48;5;0m3\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0mq\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0ms\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0ml\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mW\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0m9\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mZ\x1b[0m\x1b[38;5;78m\x1b[1m\x1b[48;5;0m6\x1b[0m
    >>> setup(dark_theme=False)
    >>> ø * b"asd"
    \x1b[38;5;2m\x1b[1m\x1b[48;5;15mL\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15ms\x1b[0m\x1b[38;5;22m\x1b[1m\x1b[48;5;15mx\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15mC\x1b[0m\x1b[38;5;22m\x1b[1m\x1b[48;5;15ma\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15mj\x1b[0m\x1b[38;5;22m\x1b[1m\x1b[48;5;15ml\x1b[0m\x1b[38;5;28m\x1b[1m\x1b[48;5;15mK\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15m8\x1b[0m\x1b[38;5;64m\x1b[1m\x1b[48;5;15m3\x1b[0m\x1b[38;5;70m\x1b[1m\x1b[48;5;15m0\x1b[0m\x1b[38;5;64m\x1b[1m\x1b[48;5;15mA\x1b[0m\x1b[38;5;23m\x1b[1m\x1b[48;5;15mK\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15mq\x1b[0m\x1b[38;5;70m\x1b[1m\x1b[48;5;15mt\x1b[0m\x1b[38;5;58m\x1b[1m\x1b[48;5;15mU\x1b[0m\x1b[38;5;2m\x1b[1m\x1b[48;5;15m5\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15mv\x1b[0m\x1b[38;5;22m\x1b[1m\x1b[48;5;15m0\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15mC\x1b[0m\x1b[38;5;22m\x1b[1m\x1b[48;5;15m9\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15mY\x1b[0m\x1b[38;5;22m\x1b[1m\x1b[48;5;15mV\x1b[0m\x1b[38;5;28m\x1b[1m\x1b[48;5;15m9\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15mb\x1b[0m\x1b[38;5;64m\x1b[1m\x1b[48;5;15mQ\x1b[0m\x1b[38;5;70m\x1b[1m\x1b[48;5;15mn\x1b[0m\x1b[38;5;64m\x1b[1m\x1b[48;5;15mZ\x1b[0m\x1b[38;5;23m\x1b[1m\x1b[48;5;15mJ\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15m1\x1b[0m\x1b[38;5;70m\x1b[1m\x1b[48;5;15mw\x1b[0m\x1b[38;5;58m\x1b[1m\x1b[48;5;15mG\x1b[0m\x1b[38;5;2m\x1b[1m\x1b[48;5;15m3\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15mq\x1b[0m\x1b[38;5;22m\x1b[1m\x1b[48;5;15ms\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15ml\x1b[0m\x1b[38;5;22m\x1b[1m\x1b[48;5;15mW\x1b[0m\x1b[38;5;34m\x1b[1m\x1b[48;5;15m9\x1b[0m\x1b[38;5;22m\x1b[1m\x1b[48;5;15mZ\x1b[0m\x1b[38;5;28m\x1b[1m\x1b[48;5;15m6\x1b[0m
    """
    bgcolor = colored.bg("#000000") if dark else colored.bg("#FFFFFF")
    fgcolor = f"#{hex(fgr)[2:].rjust(2, '0')}{hex(fgg)[2:].rjust(2, '0')}{hex(fgb)[2:].rjust(2, '0')}"
    return stylize(txt, colored.fg(fgcolor) + colored.attr("bold") + bgcolor)


def lim(x):
    return min(255, max(0, x))


def id2ansi(id, ampl=0.8, change=0.44):
    xl, xd = id2rgb(id, ampl, change)
    rgb_light, rgb_dark = xl[1:], xd[1:]
    str_light = [paint(l, *rgb, dark=False) for l, rgb in zip(id, rgb_light)]
    str_dark = [paint(l, *rgb, dark=True) for l, rgb in zip(id, rgb_dark)]
    return "".join(str_light), "".join(str_dark)


def id2rgb(id, ampl=0.8, change=0.44):
    digits = len(id)
    numbers = md5(id.encode()).digest()
    margin = 64
    fgr = margin + numbers[1] * ampl
    fgg = margin + numbers[2] * ampl
    fgb = margin + numbers[3] * ampl
    nnn = numbers * (digits * 3 // 2)
    res = []
    for dark in [False, True]:
        out = []
        bgr, bgg, bgb = 0, 0, 0
        for dr, dg, db, _ in zip(nnn, nnn[1:], nnn[2:], id):
            r = max(margin, lim(fgr + change * (dr - 128)))
            g = max(margin, lim(fgg + change * (dg - 128)))
            b = max(margin, lim(fgb + change * (db - 128)))
            if not dark:
                r = r - 130
                g = g - 130
                b = b - 130
                if r < 0 or g < 0 or b < 0:
                    worst = min([r, g, b])
                    r -= worst
                    g -= worst
                    b -= worst
            out.append([int(r), int(g), int(b)])
            bgr += r
            bgg += g
            bgb += b
        bgr = int(255 - bgr / digits)
        bgg = int(255 - bgg / digits)
        bgb = int(255 - bgb / digits)
        res.append([[bgr, bgg, bgb]] + out)
    return res


def ansi2html(ansi, **kwargs):
    r"""
    >>> from hosh import Hosh
    >>> Hosh(b"asd").ansi
    '\x1b[38;5;71m\x1b[1m\x1b[48;5;0mL\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0ms\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mx\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0mC\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0ma\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0mj\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0ml\x1b[0m\x1b[38;5;78m\x1b[1m\x1b[48;5;0mK\x1b[0m\x1b[38;5;119m\x1b[1m\x1b[48;5;0m8\x1b[0m\x1b[38;5;113m\x1b[1m\x1b[48;5;0m3\x1b[0m\x1b[38;5;113m\x1b[1m\x1b[48;5;0m0\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mA\x1b[0m\x1b[38;5;72m\x1b[1m\x1b[48;5;0mK\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0mq\x1b[0m\x1b[38;5;149m\x1b[1m\x1b[48;5;0mt\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mU\x1b[0m\x1b[38;5;71m\x1b[1m\x1b[48;5;0m5\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0mv\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0m0\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0mC\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0m9\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0mY\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mV\x1b[0m\x1b[38;5;78m\x1b[1m\x1b[48;5;0m9\x1b[0m\x1b[38;5;119m\x1b[1m\x1b[48;5;0mb\x1b[0m\x1b[38;5;113m\x1b[1m\x1b[48;5;0mQ\x1b[0m\x1b[38;5;113m\x1b[1m\x1b[48;5;0mn\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mZ\x1b[0m\x1b[38;5;72m\x1b[1m\x1b[48;5;0mJ\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0m1\x1b[0m\x1b[38;5;149m\x1b[1m\x1b[48;5;0mw\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mG\x1b[0m\x1b[38;5;71m\x1b[1m\x1b[48;5;0m3\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0mq\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0ms\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0ml\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mW\x1b[0m\x1b[38;5;83m\x1b[1m\x1b[48;5;0m9\x1b[0m\x1b[38;5;107m\x1b[1m\x1b[48;5;0mZ\x1b[0m\x1b[38;5;78m\x1b[1m\x1b[48;5;0m6\x1b[0m'
    >>> print(Hosh(b"dsa").html)  # doctest: +NORMALIZE_WHITESPACE
    <style type="text/css">
     .ansi2html-content { display: inline; white-space: pre-wrap; word-wrap: break-word; }
    .body_foreground { color: #AAAAAA; }
    .body_background { background-color: #000000; }
    .inv_foreground { color: #000000; }
    .inv_background { background-color: #AAAAAA; }
    .ansi1 { font-weight: bold; }
    .ansi48-0 { background-color: #000316; }
    .ansi38-133 { color: #af5faf; }
    .ansi38-134 { color: #af5fd7; }
    .ansi38-170 { color: #d75fd7; }
    .ansi38-103 { color: #8787af; }
    .ansi38-104 { color: #8787d7; }
    .ansi38-138 { color: #af8787; }
    .ansi38-139 { color: #af87af; }
    .ansi38-140 { color: #af87d7; }
    .ansi38-141 { color: #af87ff; }
    .ansi38-175 { color: #d787af; }
    .ansi38-176 { color: #d787d7; }
    .ansi38-110 { color: #87afd7; }
    .ansi38-144 { color: #afaf87; }
    .ansi38-146 { color: #afafd7; }
    .ansi38-247 { color: #9e9e9e; }
    </style>
    <pre class="ansi2html-content"><span class="ansi38-139"></span><span class="ansi1 ansi38-139"></span><span class="ansi1 ansi38-139 ansi48-0">v</span><span class="ansi38-140"></span><span class="ansi1 ansi38-140"></span><span class="ansi1 ansi38-140 ansi48-0">1</span><span class="ansi38-141"></span><span class="ansi1 ansi38-141"></span><span class="ansi1 ansi38-141 ansi48-0">F</span><span class="ansi38-144"></span><span class="ansi1 ansi38-144"></span><span class="ansi1 ansi38-144 ansi48-0">p</span><span class="ansi38-170"></span><span class="ansi1 ansi38-170"></span><span class="ansi1 ansi38-170 ansi48-0">b</span><span class="ansi38-110"></span><span class="ansi1 ansi38-110"></span><span class="ansi1 ansi38-110 ansi48-0">b</span><span class="ansi38-175"></span><span class="ansi1 ansi38-175"></span><span class="ansi1 ansi38-175 ansi48-0">e</span><span class="ansi38-140"></span><span class="ansi1 ansi38-140"></span><span class="ansi1 ansi38-140 ansi48-0">L</span><span class="ansi38-247"></span><span class="ansi1 ansi38-247"></span><span class="ansi1 ansi38-247 ansi48-0">z</span><span class="ansi38-134"></span><span class="ansi1 ansi38-134"></span><span class="ansi1 ansi38-134 ansi48-0">Y</span><span class="ansi38-103"></span><span class="ansi1 ansi38-103"></span><span class="ansi1 ansi38-103 ansi48-0">-</span><span class="ansi38-138"></span><span class="ansi1 ansi38-138"></span><span class="ansi1 ansi38-138 ansi48-0">M</span><span class="ansi38-133"></span><span class="ansi1 ansi38-133"></span><span class="ansi1 ansi38-133 ansi48-0">3</span><span class="ansi38-104"></span><span class="ansi1 ansi38-104"></span><span class="ansi1 ansi38-104 ansi48-0">x</span><span class="ansi38-146"></span><span class="ansi1 ansi38-146"></span><span class="ansi1 ansi38-146 ansi48-0">a</span><span class="ansi38-176"></span><span class="ansi1 ansi38-176"></span><span class="ansi1 ansi38-176 ansi48-0">Y</span><span class="ansi38-139"></span><span class="ansi1 ansi38-139"></span><span class="ansi1 ansi38-139 ansi48-0">9</span><span class="ansi38-140"></span><span class="ansi1 ansi38-140"></span><span class="ansi1 ansi38-140 ansi48-0">D</span><span class="ansi38-141"></span><span class="ansi1 ansi38-141"></span><span class="ansi1 ansi38-141 ansi48-0">W</span><span class="ansi38-144"></span><span class="ansi1 ansi38-144"></span><span class="ansi1 ansi38-144 ansi48-0">E</span><span class="ansi38-170"></span><span class="ansi1 ansi38-170"></span><span class="ansi1 ansi38-170 ansi48-0">Z</span><span class="ansi38-110"></span><span class="ansi1 ansi38-110"></span><span class="ansi1 ansi38-110 ansi48-0">U</span><span class="ansi38-175"></span><span class="ansi1 ansi38-175"></span><span class="ansi1 ansi38-175 ansi48-0">O</span><span class="ansi38-140"></span><span class="ansi1 ansi38-140"></span><span class="ansi1 ansi38-140 ansi48-0">y</span><span class="ansi38-247"></span><span class="ansi1 ansi38-247"></span><span class="ansi1 ansi38-247 ansi48-0">z</span><span class="ansi38-134"></span><span class="ansi1 ansi38-134"></span><span class="ansi1 ansi38-134 ansi48-0">8</span><span class="ansi38-103"></span><span class="ansi1 ansi38-103"></span><span class="ansi1 ansi38-103 ansi48-0">g</span><span class="ansi38-138"></span><span class="ansi1 ansi38-138"></span><span class="ansi1 ansi38-138 ansi48-0">S</span><span class="ansi38-133"></span><span class="ansi1 ansi38-133"></span><span class="ansi1 ansi38-133 ansi48-0">V</span><span class="ansi38-104"></span><span class="ansi1 ansi38-104"></span><span class="ansi1 ansi38-104 ansi48-0">h</span><span class="ansi38-146"></span><span class="ansi1 ansi38-146"></span><span class="ansi1 ansi38-146 ansi48-0">S</span><span class="ansi38-176"></span><span class="ansi1 ansi38-176"></span><span class="ansi1 ansi38-176 ansi48-0">A</span><span class="ansi38-139"></span><span class="ansi1 ansi38-139"></span><span class="ansi1 ansi38-139 ansi48-0">C</span><span class="ansi38-140"></span><span class="ansi1 ansi38-140"></span><span class="ansi1 ansi38-140 ansi48-0">g</span><span class="ansi38-141"></span><span class="ansi1 ansi38-141"></span><span class="ansi1 ansi38-141 ansi48-0">2</span><span class="ansi38-144"></span><span class="ansi1 ansi38-144"></span><span class="ansi1 ansi38-144 ansi48-0">H</span><span class="ansi38-170"></span><span class="ansi1 ansi38-170"></span><span class="ansi1 ansi38-170 ansi48-0">L</span><span class="ansi38-110"></span><span class="ansi1 ansi38-110"></span><span class="ansi1 ansi38-110 ansi48-0">t</span><span class="ansi38-175"></span><span class="ansi1 ansi38-175"></span><span class="ansi1 ansi38-175 ansi48-0">F</span><span class="ansi38-140"></span><span class="ansi1 ansi38-140"></span><span class="ansi1 ansi38-140 ansi48-0">2</span></pre>
    >>> print(Hosh(b"asd").html)  # doctest: +NORMALIZE_WHITESPACE
    <style type="text/css">
     .ansi2html-content { display: inline; white-space: pre-wrap; word-wrap: break-word; }
    .body_foreground { color: #AAAAAA; }
    .body_background { background-color: #000000; }
    .inv_foreground { color: #000000; }
    .inv_background { background-color: #AAAAAA; }
    .ansi1 { font-weight: bold; }
    .ansi48-0 { background-color: #000316; }
    .ansi38-71 { color: #5faf5f; }
    .ansi38-72 { color: #5faf87; }
    .ansi38-107 { color: #87af5f; }
    .ansi38-78 { color: #5fd787; }
    .ansi38-113 { color: #87d75f; }
    .ansi38-149 { color: #afd75f; }
    .ansi38-83 { color: #5fff5f; }
    .ansi38-119 { color: #87ff5f; }
    </style>
    <pre class="ansi2html-content"><span class="ansi38-71"></span><span class="ansi1 ansi38-71"></span><span class="ansi1 ansi38-71 ansi48-0">L</span><span class="ansi38-83"></span><span class="ansi1 ansi38-83"></span><span class="ansi1 ansi38-83 ansi48-0">s</span><span class="ansi38-107"></span><span class="ansi1 ansi38-107"></span><span class="ansi1 ansi38-107 ansi48-0">x</span><span class="ansi38-83"></span><span class="ansi1 ansi38-83"></span><span class="ansi1 ansi38-83 ansi48-0">C</span><span class="ansi38-107"></span><span class="ansi1 ansi38-107"></span><span class="ansi1 ansi38-107 ansi48-0">a</span><span class="ansi38-83"></span><span class="ansi1 ansi38-83"></span><span class="ansi1 ansi38-83 ansi48-0">j</span><span class="ansi38-107"></span><span class="ansi1 ansi38-107"></span><span class="ansi1 ansi38-107 ansi48-0">l</span><span class="ansi38-78"></span><span class="ansi1 ansi38-78"></span><span class="ansi1 ansi38-78 ansi48-0">K</span><span class="ansi38-119"></span><span class="ansi1 ansi38-119"></span><span class="ansi1 ansi38-119 ansi48-0">8</span><span class="ansi38-113"></span><span class="ansi1 ansi38-113"></span><span class="ansi1 ansi38-113 ansi48-0">3</span><span class="ansi38-113"></span><span class="ansi1 ansi38-113"></span><span class="ansi1 ansi38-113 ansi48-0">0</span><span class="ansi38-107"></span><span class="ansi1 ansi38-107"></span><span class="ansi1 ansi38-107 ansi48-0">A</span><span class="ansi38-72"></span><span class="ansi1 ansi38-72"></span><span class="ansi1 ansi38-72 ansi48-0">K</span><span class="ansi38-83"></span><span class="ansi1 ansi38-83"></span><span class="ansi1 ansi38-83 ansi48-0">q</span><span class="ansi38-149"></span><span class="ansi1 ansi38-149"></span><span class="ansi1 ansi38-149 ansi48-0">t</span><span class="ansi38-107"></span><span class="ansi1 ansi38-107"></span><span class="ansi1 ansi38-107 ansi48-0">U</span><span class="ansi38-71"></span><span class="ansi1 ansi38-71"></span><span class="ansi1 ansi38-71 ansi48-0">5</span><span class="ansi38-83"></span><span class="ansi1 ansi38-83"></span><span class="ansi1 ansi38-83 ansi48-0">v</span><span class="ansi38-107"></span><span class="ansi1 ansi38-107"></span><span class="ansi1 ansi38-107 ansi48-0">0</span><span class="ansi38-83"></span><span class="ansi1 ansi38-83"></span><span class="ansi1 ansi38-83 ansi48-0">C</span><span class="ansi38-107"></span><span class="ansi1 ansi38-107"></span><span class="ansi1 ansi38-107 ansi48-0">9</span><span class="ansi38-83"></span><span class="ansi1 ansi38-83"></span><span class="ansi1 ansi38-83 ansi48-0">Y</span><span class="ansi38-107"></span><span class="ansi1 ansi38-107"></span><span class="ansi1 ansi38-107 ansi48-0">V</span><span class="ansi38-78"></span><span class="ansi1 ansi38-78"></span><span class="ansi1 ansi38-78 ansi48-0">9</span><span class="ansi38-119"></span><span class="ansi1 ansi38-119"></span><span class="ansi1 ansi38-119 ansi48-0">b</span><span class="ansi38-113"></span><span class="ansi1 ansi38-113"></span><span class="ansi1 ansi38-113 ansi48-0">Q</span><span class="ansi38-113"></span><span class="ansi1 ansi38-113"></span><span class="ansi1 ansi38-113 ansi48-0">n</span><span class="ansi38-107"></span><span class="ansi1 ansi38-107"></span><span class="ansi1 ansi38-107 ansi48-0">Z</span><span class="ansi38-72"></span><span class="ansi1 ansi38-72"></span><span class="ansi1 ansi38-72 ansi48-0">J</span><span class="ansi38-83"></span><span class="ansi1 ansi38-83"></span><span class="ansi1 ansi38-83 ansi48-0">1</span><span class="ansi38-149"></span><span class="ansi1 ansi38-149"></span><span class="ansi1 ansi38-149 ansi48-0">w</span><span class="ansi38-107"></span><span class="ansi1 ansi38-107"></span><span class="ansi1 ansi38-107 ansi48-0">G</span><span class="ansi38-71"></span><span class="ansi1 ansi38-71"></span><span class="ansi1 ansi38-71 ansi48-0">3</span><span class="ansi38-83"></span><span class="ansi1 ansi38-83"></span><span class="ansi1 ansi38-83 ansi48-0">q</span><span class="ansi38-107"></span><span class="ansi1 ansi38-107"></span><span class="ansi1 ansi38-107 ansi48-0">s</span><span class="ansi38-83"></span><span class="ansi1 ansi38-83"></span><span class="ansi1 ansi38-83 ansi48-0">l</span><span class="ansi38-107"></span><span class="ansi1 ansi38-107"></span><span class="ansi1 ansi38-107 ansi48-0">W</span><span class="ansi38-83"></span><span class="ansi1 ansi38-83"></span><span class="ansi1 ansi38-83 ansi48-0">9</span><span class="ansi38-107"></span><span class="ansi1 ansi38-107"></span><span class="ansi1 ansi38-107 ansi48-0">Z</span><span class="ansi38-78"></span><span class="ansi1 ansi38-78"></span><span class="ansi1 ansi38-78 ansi48-0">6</span></pre>
    """
    conv = Ansi2HTMLConverter(
        # inline=False,
        dark_bg=GLOBAL["dark_theme"],
        # line_wrap=True,
        # linkify=False,
        # escaped=True,
        # markup_lines=False,
        **kwargs
    )
    html = conv.convert(ansi, full=True, ensure_trailing_newline=False)
    html = html.replace("span style=\"", "span style=\"font-family: monospace; ")
    style = BeautifulSoup(html, "html.parser").find('style').prettify()
    content = "".join(str(x) for x in BeautifulSoup(html, "html.parser").find('body').contents)
    return style + content.replace("\n", "")
