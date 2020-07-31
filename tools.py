__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"

import datetime
import time

from pip._vendor.colorama import Fore


class ColorMapping:
    #todo bring the ifs from task in here?!?
    def __init__(self):
        self.mapping = {}


class RedGreenHexColorMapping(ColorMapping):
    """
    generates color transition from red to green,
    to save computation it mapps his answers
    0:"#FF0000", 100:"00FF00"
    """
    #todo make a more darker color switch
    def __init__(self):
        super().__init__()
        self.mapping.update({0:"#FF0000", 100:"#00FF00"})

    def __call__(self, percentage, *args, **kwargs):
        """
        generates color transition from red to green,
        to save computation it mapps his answers
        0:"#FF0000", 100:"00FF00"
        """
        try:
            return self.mapping[percentage]
        except KeyError:
            color_string = self._redGreenHexColor(percentage)
            self.mapping[percentage] = color_string
            return color_string

    @staticmethod
    def _redGreenHexColor(percentage:float):
        """
        :param percentage: float from 0 to 100
        :return: color hexstring ranging from "#FF0000"(red) at 100
                to "#00FF00"(green) at 0
        """
        def hexStr(number:int):
            hex_str = hex(number)
            hex_str = hex_str.replace("0x", "")
            if len(hex_str) < 2:
                return "0" + hex_str
            return hex_str

        percentage = int(percentage)
        green = int(255 / 100 * percentage)
        red = int(255 / 100 * (100 - percentage))

        return "#" + hexStr(red) + hexStr(green) + "00"


def nowDateTime():
    """
    :return:datetime.datetime of "right now" tuple(yyyy, mm, dd, hh, mm, ss)
    """
    return datetime.datetime(*time.localtime()[:6])


def printMatrix(casenumber, matrix):
    """debug help print"""
    f = Fore.YELLOW
    print(f"{f}matrix {casenumber}")
    for list_h in matrix:
        print(f"{list_h}")
        print(f"{Fore.RESET}")

