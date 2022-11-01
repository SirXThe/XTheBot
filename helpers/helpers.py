"""
XTheBot
Copyright (C) 2022  XThe

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from sympy import sympify
import logging


def check_numbers(n):
    if any(a.isnumeric() for a in n):
        return
    else:
        return n.upper()


def check_letters(n):
    try:
        if any(a.isalpha() for a in n):
            return
        else:
            return int(sympify(n))
    except Exception:
        logging.warning(f"[Counting] Exception at check_letters: {Exception}")
        return


def check_roman(n):
    number = {c for c in n.upper()}
    valid = {c for c in "MDCLXVI()"}
    if not number - valid:
        return n.upper()
    else:
        return


def fibonacci(n: int):
    if n < 0:
        return
    elif n == 0:
        return 0
    elif n == 1 or n == 2:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def roman(n: int):
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


def letters(n: int):
    if n <= 0:
        return
    string = ''
    while n:
        temp = n % 26
        if temp == 0:
            temp = 26
        letter = chr(ord('A') + temp - 1)
        string = letter + string
        n = int((n - 1) / 26)
    return string
