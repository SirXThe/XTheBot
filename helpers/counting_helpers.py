#  XTheBot
#  Copyright (C) 2022  XThe
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from sympy import sympify
import logging


def containsNumber(n):
    if any(c.isnumeric() for c in n):
        return
    else:
        return n.upper()


def containsLetter(n):
    try:
        if any(c.isalpha() for c in n):
            return
        else:
            return int(sympify(n))
    except Exception:
        logging.warning(f"[Counting] Exception at containsLetter: {Exception}")
        return


def isRoman(n):
    number = {c for c in n.upper()}
    valid = {c for c in "MDCLXVI()"}
    if not number - valid:
        return n.upper()
    else:
        return


def Fibonacci(n: int):
    if n < 0:
        return
    elif n == 0:
        return 0
    elif n == 1 or n == 2:
        return 1
    else:
        return Fibonacci(n - 1) + Fibonacci(n - 2)


def Roman(n: int):
    if n <= 0:
        return
    res = ""
    table = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]
    for cap, number in table:
        d, m = divmod(n, cap)
        res += number * d
        n = m
    return res


def Letter(n: int):
    if n <= 0:
        return
    res = ''
    while n:
        temp = n % 26
        if temp == 0:
            temp = 26
        letter = chr(ord('A') + temp - 1)
        res += letter
        n = int((n - 1) / 26)
    return res
