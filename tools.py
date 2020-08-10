__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"

import datetime
import time

from pip._vendor.colorama import Fore


class ColorTransistor:
    def __init__(self, color_scheme:dict=None, transition_scheme=((0, 185), (220, 0), (0, 0))):
        """
        :param color_scheme: mapping for predefined colors
        :param transition_scheme: red-green-blue 255max each
                                  (zero-percent-representation, hundred-percentage-representage)
        """
        base_scheme = {0:"#B90000", 100:"#00DC00", "completed":"#004400", "no_end": None, "same_day": "#BBBB00",
                       "expired": "#AF14AF", "running_out": "#880000"}
        self.mapping = color_scheme if color_scheme else base_scheme
        self.transition_scheme = transition_scheme


    @staticmethod
    def hexStr(number:float):
        hex_str = hex(int(number))
        hex_str = hex_str.replace("0x", "")
        if len(hex_str) < 2:
            return "0" + hex_str
        return hex_str


    def transition(self, task,):
        """
        :param task:
        :return: corresponding frame-hex-color to time percentage of task
        """
        percentage:int = task.sTimePercentage()
        hex_color_string = "#"

        for zero, one in self.transition_scheme:
            range_her = abs(one - zero)
            if zero == one:
                hex_color_string += self.hexStr(zero)
            if zero < one:
                hex_color_string += self.hexStr(range_her / 100 * (100 - percentage))
            if zero > one:
                hex_color_string += self.hexStr(range_her / 100 * percentage)

        self.mapping[percentage] = hex_color_string
        return hex_color_string


    def __call__(self, task, *args, **kwargs):

        if task.sCompleted() == 100:
            return self.mapping["completed"]

        if not task.sEnde():
            return self.mapping["no_end"]

        if task.sStart() == task.sEnde():
            return self.mapping["same_day"]

        if task.sRemainingMinutes() <= 0:
            return self.mapping["expired"]

        if task.sRemainingMinutes() < 720:
            # print(f"#10921 {task.sRemainingMinutes()}")
            return self.mapping["running_out"]

        try:
            return self.mapping[task.sTimePercentage()]
        except KeyError:
            return self.transition(task=task)




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

