__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"

import os
import pickle
import subprocess
from locale import getdefaultlocale

from gui_elements import OptionWindow
from internationalisation import inter


class Option:
    def __init__(self, file_path):

        self.file_path = file_path

        if not os.path.exists(file_path):
            self._setInitialSettings()
        else:
            self.loadSettings()

    def sSettings(self):
        """returns dict of all values wich makes up program settings"""
        settings = {"directorys":{"main_folder": self.main_folder, "standard_main_folder":self.standard_main_folder,
                    "result_folder":self.result_folder, "autosave_folder":self.autosave_folder},
                    "autosave_amount":self.autosave_amount, "autosave_amount_type":self.autosave_amount_type,
                    "language":self.language, "disabled_folder_usage":self.disabled_folder_usage,
                    "autosave_handling":self.autosave_handling}
        return settings

    def sMainFolder(self):
        return self.main_folder
    def sResultFolder(self):
        return self.result_folder
    def sAutosaveFolder(self):
        return self.autosave_folder
    def sStandardMainFolder(self):
        return self.standard_main_folder
    def sStandardResultFolder(self):
        return self._standardProjectFolder(self.standard_main_folder)
    def sStandardAutosaveFolder(self):
        return self._standardAutoSaveFolder(self.standard_main_folder)
    def sAutosaveAmount(self):
        return self.autosave_amount
    def sAutosaveAmountType(self):
        return self.autosave_amount_type
    def sLanguage(self):
        return self.language
    def sDisabledFolderUsage(self):
        return self.disabled_folder_usage
    def sUserFolderUsage(self):
        return True if self.disabled_folder_usage == "std" else False
    def sAutoSaveHandling(self):
        return self.autosave_handling

    def _oneOfTwo(self, either_true, or_false, condition_one="disabled_folder_usage", condition_two="std"):
        """just beats redundancy """
        if self.__getattribute__(condition_one) == condition_two:
            return either_true()
        else:
            return or_false()
    def sUsedMainFolder(self):
        return self._oneOfTwo(self.sMainFolder, self.sStandardMainFolder)
    def sUsedResultFolder(self):
        return self._oneOfTwo(self.sResultFolder, self.sStandardResultFolder)
    def sUsedAutosavePath(self):
        return self._oneOfTwo(self.sAutosaveFolder, self.sStandardAutosaveFolder)

    def _setInternationalisationLanguage(self, language):
        """
        sets inter-language for whole program
        :return:
        """
        inter.setLanguage(language=language)

    def _systemLanguageAbbreviation(self):
        """
        :return:str "de", "en"... etc corresponding to system settings
        """
        return getdefaultlocale()[0][:2]

    def loadSettings(self):
        """updates self to old saved settings"""
        with open(self.file_path, "rb") as fh:
            saved_options = pickle.load(fh)
        self.__dict__.update(saved_options.__dict__)

    def saveSettings(self):
        """saves self"""
        with open(self.file_path, "wb") as fh:
            pickle.dump(self, fh)

    def _standardMainFolder(self):
        """gets "user/documents" folder and os.joins it with "TaskAttack" """
        try:
            dir_h =  subprocess.check_output(["xdg-user-dir", "DOCUMENTS"], universal_newlines=True).strip()
        except:
            dir_h = subprocess.check_output(["xdg-user-dir"], universal_newlines=True).strip()
        return os.path.join(dir_h, "TaskAttack")

    def _standardProjectFolder(self, main_folder: str):
        """creates language-string dependent project-folder in user/documents folder"""
        return os.path.join(main_folder, inter.projects)

    def _standardAutoSaveFolder(self, main_folder):
        """os.path.join(main_folder, "autosave")"""
        return os.path.join(main_folder, "autosave")

    def _systemLanguage(self, language_abbreviation:str):
        """returns full language word, "deutsch", "english", etc..."""
        return inter.sLanguageAbreviationMapping().get(self.language_abbreviation, "english")

    def _setInitialSettings(self):
        """sets initial options, dependent on system language and settings"""
        self.language_abbreviation = self._systemLanguageAbbreviation()
        self.language = self._systemLanguage(language_abbreviation=self.language_abbreviation)
        self._setInternationalisationLanguage(language=self.language)
        self.main_folder = self.standard_main_folder = self._standardMainFolder()
        self.result_folder = self._standardProjectFolder(self.main_folder)
        self.autosave_folder = self._standardAutoSaveFolder(self.main_folder)
        self.autosave_amount = 10
        self.autosave_amount_type = inter.pieces  # todo this may be a weak desing
        self.disabled_folder_usage = "ind"
        self.autosave_handling = True

    def getSettingsFromUser(self):
        """Starts option window and fetches user input, integrates them in itself, and saves settings"""
        settings = OptionWindow().optionWindow(settings=self.sSettings())
        if settings:
            #print(f"self dict: {self.__dict__}")
            print(f"updd dict: {settings}")
            self.__dict__.update(settings)
            self.saveSettings()
            print(f"#09923 self.dict: {self.__dict__}")



if __name__ == '__main__':
    test1 = Option("options.tas")
    test1.getSettingsFromUser()
    test1.saveSettings()
    test2 = Option("options.tas")
    test2.getSettingsFromUser()
    test2.saveSettings()
    test3 = Option("options.tas")
    test3.getSettingsFromUser()
    test3.saveSettings()