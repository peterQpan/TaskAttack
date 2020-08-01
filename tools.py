__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"

import datetime
import time

from pip._vendor.colorama import Fore


class ColorMapping:
    def __init__(self):
        self.mapping = {}


class RedGreenHexColorMapping(ColorMapping):
    # todo beauty--->
    # todo dev make this class better inheritable or changeable for various different color schemes
    """
    generates color transition from red to green,
    to save computation it mapps his answers
    0:"#FF0000", 100:"00FF00"
    """
    def __init__(self):
        super().__init__()
        self.mapping.update({0:"#B90000", 100:"#00DC00"})

    def __call__(self, task, *args, **kwargs):
        """
        generates color transition from red to green,
        to save computation it mapps his answers
        0:"#FF0000", 100:"00FF00"
        """

        """
        :return: i.e. "#FF0000" hexstring_color which indicates the approximation to the deadline date
                or none if there is no deadline
        """
        # todo beauty bring all hex colors in intercangable dict
        if task.sCompleted() == 100:
            return "#004400"

        if not task.sEnde():
            return None

        if task.sStart() == task.sEnde():
            return "#BBBB00" #yellow

        if task.sRemainingMinutes() <= 0:
            return "#AF14AF" #pink

        if task.sRemainingMinutes() < 21600:
            return "#880000" #dark red


        complete_time = task.ende - task.start
        complete_minutes = complete_time.total_seconds() // 60
        percentage = 100 / complete_minutes * task.sRemainingMinutes()

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
        green = int(220 / 100 * percentage)
        red = int(185 / 100 * (100 - percentage))
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

