__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"

import datetime
import os
import sys
import threading
import time
from os import getcwd

from pip._vendor.colorama import Fore

from internationalisation import inter


class DebugPrinter:
    def __init__(self, file_name="tak_debug"):
        self._fh = open(file_name, "w")
        sys.stderr = self._fh
        sys.stderr = self._fh

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
        """turns float in an two figure hex string"""
        hex_str = hex(int(number))
        hex_str = hex_str.replace("0x", "")
        if len(hex_str) < 2:
            return "0" + hex_str
        return hex_str

    def transition(self, task,):
        """
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

    def _preDefineColors(self, task):
        """
        :return: predefined "corner" colors for edge cases or False
        """
        if not task.sEnde():
            return self.mapping["no_end"]
        elif task.sCompleted() == 100:
            return self.mapping["completed"]
        elif task.sStart() == task.sEnde():
            return self.mapping["same_day"]
        elif task.sRemainingMinutes() <= 0:
            return self.mapping["expired"]
        elif task.sRemainingMinutes() < 720:
            return self.mapping["running_out"]
        return False

    def __call__(self, task, *args, **kwargs):
        """
        :return: hex color string
        """
        predefined_colors = self._preDefineColors(task=task)
        if predefined_colors is not False:
            return predefined_colors
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

def startExternAplicationThread(file_path:str, threads:list):
    """
    starts external corresponding programm for task result file
    :param threads: list to save thread in it to prevent garbage collection and enables later referencing
    """
    thread = threading.Thread(target=os.system, args=(f"xdg-open '{file_path}'",))
    thread.start()
    threads.append(thread)

def venvAbsPath(file_path:str):
    """
    faces os.path.abspath's problems with venv
    :param file_path:
    :return:
    """
    cwd = os.getcwd()
    return cwd + file_path

def completeFilePathWithExtension(file_path, target_extension: str = ".tak"):
    """
    checks file path for ".ext" and adds it if necessary
    :param file_path: "file_path_string"
    :return: "some "file_path_string.tak"
    """
    file_name, extension = os.path.splitext(file_path)
    if not extension:
        file_path += target_extension
    return file_path

def setCWDbashFix():
    main_file_path = __file__
    main_path = os.path.split(main_file_path)
    os.chdir(main_path[0])

def eventIsNotNone(event):
    """checks event for None, Abbrechen
    :param event: sg.window.read()[0]
    :return: true if not close or Abrechen>>>inter.cancel it is dynamic
    """
    if event and event != inter.cancel:
        return True
    return False

