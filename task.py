__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"

import copy
import os
import pickle
import shutil

import tools


class Task:
    def __init__(self, name:str, description:str=None, start=None, end=None, priority=21, master=None):
        self.name = name
        self.description = description
        self.start = start if start else tools.nowDateTime()
        self.ende = end
        self.priority = priority

        self.master = master
        self.sub_tasks = []
        self._completed = 0

        self._redGreenHexColor = tools.RedGreenHexColorMapping()

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __str__(self):
        return self.sName()

    def __repr__(self):
        return f"Task: {self.sName()} {self.sStart()} {self.sCompleted()}"

    @property
    def completed(self):
        #todo bring all this into sCompleted?!?
        if not self.sub_tasks:
            # try:
            return self._completed
            # except:
            #     todo pickle versionierung lernen
                # self._completed = 0
                # return self._completed
        else:
            zaehler = sum(x.completed for x in self.sub_tasks)
            teiler = len(self.sub_tasks)
            return zaehler / teiler

    def sCompleted(self, completed:int=None):
        if completed is None:
            return self.completed
        else:
            self.completed(completed)
            #todo ?!?

    def sMastersEnde(self):
        if self.master:
            return self.master.sEnde()

    def sMastersPriority(self):
        if self.master:
            return self.master.sPriority()

    def sName(self):
        return self.name

    def sDescription(self):
        return self.description

    def sStart(self):
        return self.start

    def sEnde(self):
        return self.ende

    def sPriority(self):
        return self.priority

    def sMaster(self):
        return self.master

    def sSubTasks(self):
        return self.sub_tasks

    def sPosition(self):
        return self.position

    def sPercentage(self):
        """
        personal percentage weight of the single task in proportion to the howl project
        :return:
        """
        if self.master is None:
            return 100
        else:
            return self.master.subTaskPercentage()

    def sRemainingTimedelta(self):
        try:
            #todo some kind of mapping and time thread based actualisation since this function gets invoked 8 times
            # just for one task for window renewel circle
            print(f"#777777 time_delta: {self.ende - tools.nowDateTime()}")
            return self.ende - tools.nowDateTime()

        except TypeError:
            return None

    def sRemainingDays(self):
        if self.sRemainingTimedelta():
            return self.sRemainingTimedelta().days

    def sRemainingMinutes(self):
        if self.sRemainingTimedelta():
            return self.sRemainingTimedelta().total_seconds() // 60

    def changeCompleted(self):
        self._completed = 0 if self._completed else 100

    def addSubTask(self, name: str, description, start, ende=None, priority: int = 9):
        sub_task = self.__class__(name, description, start, ende, priority, self)
        self.sub_tasks.append(sub_task)


    def delete(self):
        self.master.deleteSubTask(self)

    def deleteSubTask(self, task):
        self.sub_tasks.remove(task)

    def allSubordinatedTasks(self):
        """
        :return: flat list all tasks hierarchically deeper than self or self
        """
        if not self.sub_tasks:
            return [self]
        else:
            all_tasks_under = []
            all_tasks_under += [x.allSubordinatedTasks() for x in self.sub_tasks]
            return all_tasks_under

    def taskDeadlineColor(self):
        """
        :return: i.e. "#FF0000" hexstring_color which indicates the approximation to the deadline date
                or none if there is no deadline
        """
        #todo all this ifs in hexcolor class?!?
        if not self.ende:
            return None

        if self.start == self.ende:
            return "#BBBB00"

        if self.sRemainingMinutes() <= 0:
            return "#AF14AF"

        if self.sRemainingDays() < 0:
            return "#BB0000"

        if self.completed == 1:
            return "#004400"

        complete_time = self.ende - self.start
        complete_minutes = complete_time.total_seconds() // 60
        percentage = 100 / complete_minutes * self.sRemainingMinutes()

        return self._redGreenHexColor(percentage)

    def HierarchyTreePositionString(self, lenght=30):
        # todo enable mapping or saving o something so that this function didnt have to run everytime,
        #  because it is runing twice alone in task frame creator, each window generation,
        #  maby ther is a even better way than mapping or saving, becaus after implementig moving tasks
        #  araound this mapping will bug araund
        """
        :return: string of tree herachie like: projectname/mastertask/mastertask/
        """
        list_h = self.hierarchyTreePositionList()[:-1]
        if list_h:
            string = "/" + "/".join(list_h)
            return string[-lenght:]
        else:
            return " "

    def hierarchyTreePositionList(self):
        """
        :return:list of str with own task hierarchy tree
        """
        if self.master:
            master_strings_list_here = self.master.hierarchyTreePositionList() + [f"{self.name}"]
            print(f"master tree here: #1234sds {master_strings_list_here}")

            return master_strings_list_here
        else:
            print(f"return onely myself.name #908uo2i3j {[self.name]}")
            return [f"{self.name}"]

    def sDataRepresentation(self):
        """
        :return:dict aller zur gui darstellung benötigten daten
        name, description, start, ende, priority, percentage, completed
        """
        dr = {"name":self.name, "description":self.description, "start": self.start, "ende": self.ende,
              "priority": self.priority, "percentage":self.sPercentage(), "completed":self.completed,
              "masters_ende":self.sMastersEnde()}
        if self.master is None:
            dr.update({"kind": "Projekt"})
        else:
            dr.update({"kind": "Aufgabe"})
        return dr

    def rowExpansion(self):
        """
        :return: needed y space to display self and all subtasks in matrix
        """
        if not self.sub_tasks:
            return 1
        else:
            return sum([sub_task.rowExpansion() for sub_task in self.sub_tasks])

    def subTaskDepth(self):
        """
        :return: needed x space to display self all subtasks in matrix
        """
        if not self.sub_tasks:
            return 1
        else:
            return max([sub_task.subTaskDepth() for sub_task in self.sub_tasks]) + 1

    def subTaskPercentage(self):
        """
        :return: the percentage of one task in proportion to the howl project
        """
        return self.sPercentage() / len(self.sub_tasks)

    def recognizeMatrixPosition(self, depth, span):
        """
        speichert eigene koordinaten, darstellungsmatrix als self.position und gibt, subtask_koordinaten
        an subtasks weiter, damit diese ihre position speichern konnen
        :param depth: column koordinate
        :param span: row koordinate
        :return:
        """

        self.position = (depth, span)
        for sub_task in self.sub_tasks:
            sub_task.recognizeMatrixPosition(depth=depth+1, span=span)
            span += sub_task.rowExpansion()

    def update(self, name:str, description, start, ende=None, priority=9,
               # completed=0
               ):
        self.name = name
        self.description = description
        print(f"start zuerst {self.start}")
        self.start = start
        print(f"start danach:a {self.start}")
        self.ende = ende
        self.priority = priority
        #self.completed = completed

    def takePosition(self, base_matrix):
        """
        orders task to take own position in base_matrix, orders sub_task to do the same
        :param base_matrix: list of list
        :return: base_matrix wit tasks at destinct places
        """
        if self.sub_tasks:
            [sub.takePosition(base_matrix) for sub in self.sub_tasks]
        x, y = self.sPosition()
        base_matrix[y][x] = self
        return base_matrix


class Taskmanager:
    def __init__(self):
        self.task_matrix = None
        self.reset()

    def sTaskMatrix(self):
        return self.task_matrix

    def reset(self):
        """task to perform if task manager has to reset i.e. new or load
        """
        self.projekts = []
        self.task_matrix = None

    def save(self, filename="projects.bin"):
        # if not os.path.isdir("autosave"):      # todo in code cleanup and debug brance
        #     os.mkdir("autosave")

        with open(filename, "wb") as fh:
            for projekt in self.projekts:
                pickle.dump(projekt, fh)
                print(f"gespeichert: {filename}")

    def load(self, file_path="projects.bin"):
        self.reset()
        with open(file_path, "rb") as fh:
            while True:
                try:
                    project = pickle.load(fh)
                    self.projekts.append(project)
                except EOFError:
                    break

    def addProject(self, name:str, description=None, start=None, end=None, priority:int=21):
        """
        creates a new project"""
        new_project = Task(name=name, description=description, start=start, end=end, priority=priority)
        self.projekts.append(new_project)

    def columnCount(self):
        """
        :return:int amount of columns >x< needed for diplaying task-structure
        """
        try:
            return max([projekt.subTaskDepth() for projekt in self.projekts])
        except ValueError:
            print(f"noch keine projekte vorhanden")

    def rowCount(self):
        """
        :return:int amout of rows >y< needet for displaying task-structure
        """
        try:
            return sum([projekt.rowExpansion() for projekt in self.projekts])
        except ValueError:
            print(f"noch keine projekte vorhanden")

    def matrixDimensions(self):
        """
        :return: columns, rows >>> x, y of complete Display-Matrix
        """
        columns = self.columnCount()
        rows = self.rowCount()
        return columns, rows

    def baseMatrix(self):
        """
        :return: list of lists reassembling the display matrix
        """
        x, y = self.matrixDimensions()
        try:
            one_row = [0 for _ in range(x)]
            return [one_row[:] for _ in range(y)]
        except TypeError as e:
            if e.__str__() == "can't multiply sequence by non-int of type 'NoneType'":
                return [[]]
            else:
                raise e

    def createTaskMatix(self):
        """
        orders all task in display-Matriy, so that they have their positions as the should be shown in the Gui
        :return:list_of_lists >>> the task filled display matrix
        """
        base_matrix = self.baseMatrix()
        for task in self.projekts:
            task: Task
            task.takePosition(base_matrix)
        return base_matrix

    def recognizeMatrixPositions(self):
        """commands subtasks to recognize their position in the display matrix"""
        span_here = 0
        for projekt in self.projekts:
            projekt: Task
            projekt.recognizeMatrixPosition(depth=0, span=span_here)
            span_here += projekt.rowExpansion()

    def addMasterTaskPlaceholderStrings(self, display_matrix):
        """
        adds master-tree-placeholder-str to display matrix
        :param display_matrix: task filled list of list
        :return: dask and master-string filled lost of list
        """
        display_matrix_to_work_on = copy.deepcopy(display_matrix)
        for y_index, y in enumerate(display_matrix):
            actual_task = None
            print(f"y_index: {y_index}, y: {y}")
            for x_index, x in enumerate(y):
                # print(f"x_index: {x_index}, x: {x}")
                if isinstance(x, Task):
                    all_masters_strings_list = x.HierarchyTreePositionString()
                    print(f"task_row: {x.sPosition()}, {x.sName() }all masters: {all_masters_strings_list}")
                    actual_task = ">".join(all_masters_strings_list)
                else:
                    if actual_task:
                        display_matrix_to_work_on[y_index][x_index] = actual_task
        return display_matrix_to_work_on

    def displayMatrix(self):
        """
        final function to create the finished display matrix
        :return: THEdisplay
        """
        if not self.projekts:
            return [[]]

        self.recognizeMatrixPositions()
        self.task_matrix = self.createTaskMatix()
        display_matrix = self.addMasterTaskPlaceholderStrings(self.task_matrix)
        return display_matrix


if __name__ == '__main__':
    one_task = Task(name="test_task")

