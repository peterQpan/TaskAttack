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
    """
    generates color transition from red to green,
    to save computation it mapps his answers
    0:"#FF0000", 100:"00FF00"
    """
    def __init__(self, color_scheme:dict={0:"#B90000", 100:"#00DC00", "completed":"#004400", "no_end": None,
                                          "same_day": "#BBBB00", "expired": "#AF14AF", "running_out": "#880000"}):
        # todo dev: make class complete changeable with init red_zero:red_hundred, green_zero:red_hundred,
        #  blue_zero:blue:hundred and transition_method takes this without knowing and execute color transition
        super().__init__()
        self.mapping.update(color_scheme)


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

        if task.sCompleted() == 100:
            return self.mapping["completed"]

        if not task.sEnde():
            return self.mapping["no_end"]

        if task.sStart() == task.sEnde():
            return self.mapping["same_day"]

        if task.sRemainingMinutes() <= 0:
            return self.mapping["expired"]

        if task.sRemainingMinutes() < 21600:
            return ["running_out"]


        complete_time = task.sEnde() - task.sStart()
        # todo beauty: make a Task.sCompleteTime() WHIT IN the time dependent mapping
        complete_minutes = complete_time.total_seconds() // 60
        percentage = int(100 / complete_minutes * task.sRemainingMinutes())

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

