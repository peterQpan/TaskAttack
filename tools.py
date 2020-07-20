__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"

import datetime
import json
import time
import PySimpleGUI as sg

from pip._vendor.colorama import Fore


class ColorMapping:
    def __init__(self):
        self.mapping = {}

class RedGreenHexColorMapping(ColorMapping):
    def __init__(self):
        """
        0:"#FF0000", 100:"00FF00"
        """
        super().__init__()
        self.mapping.update({100:"#FF0000", 0:"#00FF00"})

    def __call__(self, percentage, *args, **kwargs):
        try:
            return self.mapping[percentage]
        except:
            color_string = self._redGreenHexColor(percentage)
            self.mapping[percentage] = color_string
            return color_string

    def _redGreenHexColor(self, percentage:float):
        """
        :param percentage: float from 0 to 100
        :return: color hexstring ranging from "#FF0000"(red) at 100
                to "#00FF00"(green) at 0
        """
        def hexStr(number:int):
            hex_str = hex(number)
            hex_str = hex_str.replace("0x", "")
            print((f"hexstr: {hex_str}"))
            if len(hex_str) < 2:
                return "0" + hex_str
            return hex_str
        percentage = int(percentage)
        green = int(255 / 100 * (100 - percentage))
        red = int(255 / 100 * percentage)
        return "#" + hexStr(red) + hexStr(green) + "00"


def nowDT():
    return datetime.datetime(*time.localtime()[:6])


def printMatrix(casenumber, matrix):
    f = Fore.YELLOW
    print(f"{f}matrix {casenumber}")
    for list in matrix:
        print(f"{list}")
        print(f"{Fore.RESET}")

