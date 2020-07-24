__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"

import pickle


class Upgrader:
    """
    Abstract Class to make introduction of new Attributes possible
    """
    class_version = 1.0
    """class attribute to make versioning global
    starts at 1 zero is without Upgradeable """

    # todo this class is upgradable but it cant handle recursive class attributes,
    #  make a new recursive upgradeable class or try to add a recursive upgrade method

    def __init__(self):
        self.version = self.__class__.class_version

    # not needed Taskmanager takes care of saving
    # ok with single responsibility?!?
    # def save(self, file_name="test_update.bin"):
    #     with open(file_name, "wb") as fh:
    #         pickle.dump(self, fh)

    @staticmethod
    def load(file_name="test_update.bin"):
        with open(file_name, "rb") as fh:
            out = pickle.load(fh)
        if not hasattr(out, 'version'):
            out.version = 0.0
        if out.version != out.class_version:
            out.upgrade()
        return out

    def upgrade(self):
        print(f"upgrade from version {self.version}")
        if self.version < 1.0:
            self.version = 1.0
        #     self.in_version_1_0_added_atribute = "what ever"
        #     self.in_version_1_0_added_atribute2 = "what ever"
        #     print('upgrade to version 1.0')
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


class TaskUpgrader(Upgrader):
    """Abstract upgrade class for Task (able to do upgrades recursively)"""
    sub_tasks: list  # inherited then by task.Task()

    @staticmethod
    def versionSaveUnpickeling(pickle_thing):
        out = pickle.load(pickle_thing)
        if not hasattr(out, 'version'):
            out.version = 0.0
        out.upgrade()
        return out

    def upgrade(self):
        """recursiv upgrade version"""
        print(f"upgrade from version {self.version}")
        if self.version < 1.0:
            self.version = 1.0
        #     self.in_version_1_0_added_atribute = "what ever"
