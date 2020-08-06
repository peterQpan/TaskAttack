__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"

import copy
import os
import pickle
import threading
import time

import tools
from internationalisation import inter


class Task:
    def __init__(self, name:str, description:str=None, start=None, end=None, priority=21, master=None,
                 taskmanager:"Taskmanager"=None):

        self.name = name
        self.description = description
        self.start = start if start else tools.nowDateTime()
        self.ende = end
        self.priority = priority
        self.master = master
        self.taskmanager = taskmanager

        self.sub_tasks = []

        self._completed = 0
        self._remaining_timedelta = None
        self._remaining_minutes = None
        self._remaining_days = None

        self._colorSheme = tools.ColorTransistor()

    def __getstate__(self):
        state = {x:y for x,y in self.__dict__.items()}
        print(self.__dict__)
        print(state)
        #since taskmanager is an atribute of task, and task gets pickled,
        # but i woulnt taskmanager pickled as well it has to be exclude bevor,
        # i do this at the getstate-step
        state["taskmanager"] = None # out or later have to be in persistencer
        return state

    def __setstate__(self, state):
        #todo this time
        state.update({"_remeining_timedelta":None})
        self.__dict__.update(state)

    def __str__(self):
        return self.sName()

    def __repr__(self):
        return f"Task: {self.sName()} {self.sStart()} {self.sCompleted()}"

    def sCompleted(self, completed:int=None):
        """
        returns the completed percentage of an task, if value is provided, this value will be set
        """
        if self.sub_tasks:
            zaehler = sum(x.sCompleted() for x in self.sub_tasks)
            teiler = len(self.sub_tasks)
            print(f"zaehler/teiler: {zaehler /teiler}")
            return zaehler / teiler
        else:
            if completed:
                self._completed = completed
            else:
                print(self._completed)
                return self._completed

    def sMastersEnde(self):
        if self.master:
            return self.master.sEnde()

    def sMastersPriority(self):
        # todo dev install masters priority like date.end cant self.priority cant be smaller than masters priority
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
        personal percentage weight of the single task in proportion to the hole project
        :return:
        """
        if self.master is None:
            return 100
        else:
            return self.master.subTaskPercentage()

    def sRemainingTimedelta(self):
        """sets all time related values so they dont have to be computed every window renewal,
        self._remaining_timedelta gets resat to None from Master-over-all-renewal-thread, so the actuality
        is ensured, as well
        :return datetime.timedelta of tasks remaining time from now time"""
        # todo beauty: this method have to be more beautiful

        if self._remaining_timedelta is None:
            try:
                self._remaining_timedelta = self.sEnde() - tools.nowDateTime()
                self._complete_time = self.sEnde() - self.sStart()
                self._complete_minutes = self._complete_time.total_seconds() // 60
                self._remaining_minutes = self._remaining_timedelta.total_seconds() // 60
                self._remaining_days = self._remaining_timedelta.days
                self._time_percentage = int(100 / self._complete_minutes * self._remaining_minutes)
            except TypeError as e:
                print(f"#kakld89i error: {e.__traceback__}, {e.__repr__()}, {e.__traceback__.tb_lineno}")
                self._remaining_timedelta = self._remaining_minutes = False
                self._complete_time = False
                self._complete_minutes = False
                self._remaining_minutes = False
                self._remaining_days = False

        return self._remaining_timedelta

    def sCompleteTime(self):
        return self._complete_time

    def sTimePercentage(self):
        return self._time_percentage

    def sCompleteMinutes(self):
        return self._complete_minutes

    def sRemainingDays(self):
        # todo beauty ---> how to avoid need for this check
        if self._remaining_days is None:
            self.sRemainingTimedelta()
        return self._remaining_days

    def sRemainingMinutes(self):
        return self._remaining_minutes

    def resetTimedelta(self):
        # todo think should this distinguish, between None and False because of self.sRemainingTimedelta()
        self._remaining_timedelta = None

    def recursiveTimeDeltaReset(self):
        """
        method for master-time-renewal-thread, resets _remaining_timedelta,
        so anew computation is needed and executed
        """
        self.resetTimedelta()
        print(f"time delta resetted")
        [sub_task.recursiveTimeDeltaReset() for sub_task in self.sub_tasks]

    def changeCompleted(self):
        self._completed = 0 if self._completed else 100

    def addSubTask(self, name: str, description, start, ende=None, priority: int = 9):
        sub_task = self.__class__(name, description, start, ende, priority, self)
        self.sub_tasks.append(sub_task)

    def delete(self):
        try:
            self.master.deleteSubTask(self)
        except:
            self.taskmanager.deleteSubTask(task=self)


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
        return self._colorSheme(task=self)

    def HierarchyTreePositionString(self, lenght=30):
        # todo enable mapping or saving o something so that this function didnt have to run everytime,
        # todo because it is runing twice alone in task frame creator, each window generation, #todo think maby better optimize use in frame creation
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
        # todo beauty this needs some kind of mapping too, hiere it is like the problem of fibonacci-recursion,
        #  while not quadratic but redundant for sure
        if self.master:
            master_strings_list_here = self.master.hierarchyTreePositionList() + [f"{self.name}"]

            return master_strings_list_here
        else:
            return [f"{self.name}"]

    def sDataRepresentation(self):
        """
        :return:dict aller zur gui darstellung benötigten daten
        name, description, start, ende, priority, percentage, completed
        """
        dr = {"name":self.name, "description":self.description, "start": self.start, "ende": self.ende,
              "priority": self.priority, "percentage":self.sPercentage(), "completed":self.sCompleted,
              "masters_ende":self.sMastersEnde()}
        if self.master is None:
            dr.update({"kind": inter.project})
        else:
            dr.update({"kind": inter.task})
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
        try:
            return self.sPercentage() / len(self.sub_tasks)
        except:
            print(f"self percentage: {self.sPercentage()} subtasks: {self.sub_tasks}")

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

    def update(self, name:str, description, start, ende=None, priority=9):
        """updates a task with new or changed values"""
        self.name = name
        self.description = description
        self.start = start
        self.ende = ende
        self.priority = priority
        self.resetTimedelta()

    def takePosition(self, base_matrix):
        """orders task to take own position in base_matrix, orders sub_task to do the same
        :param base_matrix: list of list
        :return: base_matrix wit tasks at destinct places"""
        if self.sub_tasks:
            [sub.takePosition(base_matrix) for sub in self.sub_tasks]
        x, y = self.sPosition()
        base_matrix[y][x] = self
        return base_matrix

    def recover(self):
        """adds task back in masters sub-task-container, needed for reverse a task-deletion"""
        self.master: Task
        self.master.recoverSubtask(task=self)

    def recoverSubtask(self, task):
        self.sub_tasks.append(task)

    def setTaskManager(self, taskmanager):
        # out or later beauty hav to be in persistencer, not an automation executed by the persistencer,
        #  just the method totally unchanged for responsibility reasons
        self.taskmanager = taskmanager

    def insertClipbordTask(self, clipbord_task):
        self.sub_tasks.append(clipbord_task)

    def setMaster(self, task):
        self.master = task


class Taskmanager:
    def __init__(self):

        self.renewal_thread = None
        self.task_matrix = None
        self.reset()

    def sTaskMatrix(self):
        return self.task_matrix

    def reset(self):
        """task to perform if task manager has to reset i.e. new or load
        """
        self.sub_tasks = []
        self._side_packed_project = None
        self.task_matrix = None


    def save(self, filename="dev-auto.atk"):
        if not os.path.isdir("autosave"):
            os.mkdir("autosave")

        with open(filename, "wb") as fh:
            for projekt in self.sub_tasks:
                pickle.dump(projekt, fh)

    def load(self, file_path="dev-auto.atk"):
        self.reset()
        with open(file_path, "rb") as fh:
            while True:
                try:
                    project = pickle.load(fh)
                    project.setTaskManager(self)
                    self.sub_tasks.append(project)
                except EOFError:
                    break

    def addSubTask(self, name:str, description=None, start=None, end=None, priority:int=21):
        """
        creates a new project"""
        new_project = Task(name=name, description=description, start=start, end=end, priority=priority,
                           taskmanager=self)
        self.sub_tasks.append(new_project)
        if not self.renewal_thread:
            self.startDataDeletionForRenewalThread()

    def deleteSubTask(self, task):
        self.sub_tasks.remove(task)


    # todo dev, easyficationn, this functions have to cange to become uniform with task methods of
    #  the same kind so isolated subtask view works easily and in the same matter

    def isolatedTaskView(self, task):
        """
        isolate one task ond gives him the hole sheet space to look and work on
        :param task:
        """
        self._side_packed_project = self.sub_tasks
        task.taskmanager = self #todo beauty get a method for this
        self.sub_tasks = [task]


    def deisolateTaskView(self, *args, **kwargs):
        """
        brings isolated view back to complete tree view of all the tasks"""
        self.sub_tasks[0].taskmanager = None
        self.sub_tasks = self._side_packed_project
        self._side_packed_project = None


    def subTaskDepth(self):
        """
        :return:int amount of columns >x< needed for diplaying task-structure
        """
        try:
            return max([projekt.subTaskDepth() for projekt in self.sub_tasks])
        except ValueError:
            print(f"noch keine projekte vorhanden")

    def rowExpansion(self):
        """
        :return:int amout of rows >y< needet for displaying task-structure
        """
        try:
            return sum([projekt.rowExpansion() for projekt in self.sub_tasks])
        except ValueError:
            print(f"noch keine projekte vorhanden")

    def matrixDimensions(self):
        """
        :return: columns, rows >>> x, y of complete Display-Matrix
        """
        columns = self.subTaskDepth()
        rows = self.rowExpansion()
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
        for task in self.sub_tasks:
            task: Task
            task.takePosition(base_matrix)
        return base_matrix

    def recognizeMatrixPositions(self):
        """commands subtasks to recognize their position in the display matrix"""
        span_here = 0
        for projekt in self.sub_tasks:
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
                print(f"x_index: {x_index}, x: {x}")
                if isinstance(x, Task):
                    all_masters_strings_list = x.HierarchyTreePositionString()
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
        if not self.sub_tasks:
            return [[]]

        self.recognizeMatrixPositions()
        self.task_matrix = self.createTaskMatix()
        display_matrix = self.addMasterTaskPlaceholderStrings(self.task_matrix)
        return display_matrix

    def startDataDeletionForRenewalThread(self):
        """starts a thread that resets task-time-mapping, so actuality is ensured"""
        def renewal(subtasks):
            while True:
                time.sleep(7200)
                print(f"#09u09u recursive reset triggered in thread")
                [subtask.recursiveTimeDeltaReset() for subtask in subtasks]

        self.renewal_thread = threading.Thread(target=renewal, args=(self.sub_tasks,), daemon=True)
        self.renewal_thread.start()



if __name__ == '__main__':
    one_task = Task(name="test_task")

