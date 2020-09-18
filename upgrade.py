__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"

import os
import pickle

import tools


class Persistencer:
    """Abstract Class which handles persistence, including introducing new attributes
    for further development:
    Abstract upgrade class for Task, for unpickeling old save data with
    inadequate/insufficient attributes (able to do upgrades recursively)"""
    sub_tasks: list  # inherited then by task.Task()
    class_version = 0.2    # class attribute to make versioning global starts at 1 zero is without Upgradeable,
                           #  have to be continuously raised with actual version number# """

    def __init__(self):
        self.version = self.__class__.class_version

    def save(self, fh):
        pickle.dump(self, fh)

    def _upgrade(self):
        print(f"upgrade from version {self.version}")
        if self.version < 0.1:
            print("blau")
            self.version = 0.1
            if not self.links:
                self.links = []
        if self.version < 0.2:
            self.completedWorkReduction = tools.completedWorkReducer(refresh_time=2, completed=self._completed)

        # if self.version < 2.0:
        #     self.version = 2.0
        #     self.in_version_2_0_added_atribute = "what ever"
        #     self.in_version_2_0_added_atribute2 = "what ever"
        #     print('upgrade to version 2.0')
        # if self.version < 3.0:
        #     self.version = 3.0
        #     self.in_version_3_0_added_atribute = "what ever"
        #     self.in_version_3_0_added_atribute2 = "what ever"
        #     print('upgrade to version 3.0')
        self._recursive_update(self)

    @staticmethod
    def _properLoad(fh):
        out = pickle.load(fh)
        out.version = out.__dict__.get("version", 0.0)
        return out

    @staticmethod
    def _recursive_update(out):
        for sub_task in out.sub_tasks:
            sub_task.version = sub_task.__dict__.get("version", 0.0)
            sub_task._upgrade()

    @staticmethod
    def load(fh):
        out = Persistencer._properLoad(fh)
        if out.version != out.class_version:
            out._upgrade()
        print(f"#M-90932ß9ß0 loaded {type(out)}: {out.__dict__}")
        return out


class RenameUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        renamed_module = module
        if "taskatack" in module:
            renamed_module = module[10:]
        return super().find_class(renamed_module, name)


class ModulDirectoryNameChangeRepickeler:
    def __init__(self, file_path="autosave"):
        self.path = file_path

    def allFilesInPath(self):
        all_files = os.listdir(self.path)
        return [os.path.join(self.path, x) for x in all_files]

    def renamedLoad(self, file_path):
        with open(file_path, "rb") as fh:
            return RenameUnpickler(fh).load()

    def renamedSave(self,file_path, taskattack_save_object):
        with open(file_path, "wb") as fh:
            pickle.dump(taskattack_save_object, fh)

    def runFolder(self):
        for file_path in self.allFilesInPath():
            loaded = self.renamedLoad(file_path)
            print(f"{file_path} geladen")
            self.renamedSave(file_path,loaded)
            print(f"und wieder gespeichert")


if __name__ == '__main__':
    changer = ModulDirectoryNameChangeRepickeler("autosave")
    changer.runFolder()
