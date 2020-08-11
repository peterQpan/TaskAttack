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

        self._results = []
        self._hierarchy_tree_positions_string = None
        self._hierarchy_tree_positions = None
        self.name = name
        self.description = description
        self.start = start if start else tools.nowDateTime()
        self.ende = end
        self.priority = priority
        self.master = master
        self.taskmanager = taskmanager

        self.sub_tasks = []
        self._completed = 0

        self._colorSheme = tools.ColorTransistor()

        # MAPPINGS
        self._remaining_timedelta = None
        self._remaining_minutes = None
        self._remaining_days = None


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
        state.update({"_remeining_timedelta":None, "taskmanager":None})
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

    def sResults(self):
        return self._results

    def sCompleteTime(self):
        return self._complete_time

    def sTimePercentage(self):
        return self._time_percentage

    def sCompleteMinutes(self):
        return self._complete_minutes

    def sRemainingDays(self):
        if self._remaining_days is None:
            self.sRemainingTimedelta()
        return self._remaining_days

    def sRemainingMinutes(self):
        return self._remaining_minutes

    def _setAllTimeMappings(self):
        """computes all time related values to the time-mapping-atributes"""
        self._remaining_timedelta = self.sEnde() - tools.nowDateTime()
        self._complete_time = self.sEnde() - self.sStart()
        self._complete_minutes = self._complete_time.total_seconds() // 60
        self._remaining_minutes = self._remaining_timedelta.total_seconds() // 60
        self._remaining_days = self._remaining_timedelta.days
        self._time_percentage = int(100 / self._complete_minutes * self._remaining_minutes)


    def _setAllTimeMappingsFalse(self):
        self._remaining_timedelta = self._remaining_minutes = False
        self._complete_time = False
        self._complete_minutes = False
        self._remaining_minutes = False
        self._remaining_days = False

    def sRemainingTimedelta(self):
        """sets all time related values so they dont have to be computed every window renewal,
        self._remaining_timedelta gets resat to None from Master-over-all-renewal-thread, so the actuality
        is ensured, as well
        :return datetime.timedelta of tasks remaining time from now time"""
        if self._remaining_timedelta is None:
            try:
                self._setAllTimeMappings()
            except TypeError as e:
                print(f"#kakld89i error: {e.__traceback__}, {e.__repr__()}, {e.__traceback__.tb_lineno}")
                self._setAllTimeMappingsFalse()

        return self._remaining_timedelta

    def sResults(self):
        return self._results

    def _conditionalTimedeltaReset(self):
        """sets _remaining_timedelta to None if not False, false indicates no end date, so there is no need
        to change this"""
        if self._remaining_timedelta is not False:
            self._remaining_timedelta = None

    def recursiveConditionalTimedeltaReset(self):
        """
        method for master-time-renewal-thread, resets _remaining_timedelta conditionally,
        so anew computation is needed and executed
        """
        self._conditionalTimedeltaReset()
        print(f"time delta resetted")
        [sub_task.recursiveConditionalTimedeltaReset() for sub_task in self.sub_tasks]

    def mappingsRecursivelyAcknowledgeTaskChange(self):
        """resets "trigger"-mappings recursively, so maybe changed values get new computed/updated """
        self._mappingsAcknowledgeTaskChange()
        [sub_task.mappingsRecursivelyAcknowledgeTaskChange() for sub_task in self.sub_tasks]

    def _mappingsAcknowledgeTaskChange(self):
        """resets "trigger"-mappings, so maybe changed values get new computed/updated """
        self._remaining_timedelta = None
        self._hierarchy_tree_positions_string = None
        self._hierarchy_tree_positions = None

    def hierarchyTreePositionString(self, lenght=30):
        """
        :return: string of tree herachie like: projectname/mastertask/mastertask/
        """
        if self._hierarchy_tree_positions_string is None:
            if self.hierarchyTreePositionList()[:-1]:
                self._hierarchy_tree_positions_string = "/" + "/".join(self.hierarchyTreePositionList()[:-1])
            else:
                return " "
        return self._hierarchy_tree_positions_string[-lenght:]


    def hierarchyTreePositionList(self):
        """
        :return:list of str with own task hierarchy tree
        """
        if self.master:
            if self._hierarchy_tree_positions is None:
                self._hierarchy_tree_positions = self.master.hierarchyTreePositionList() + [f"{self.name}"]
            return self._hierarchy_tree_positions
        else:
            return [f"{self.name}"]


    def changeCompleted(self):
        self._completed = 0 if self._completed else 100

    def addSubTask(self, name: str, description, start, ende=None, priority: int = 9):
        sub_task = self.__class__(name, description, start, ende, priority, self)
        self.sub_tasks.append(sub_task)

    def delete(self):
        if self.master:
            self.master.deleteSubTask(self)
            if self.taskmanager:
                self.taskmanager.deisolateTaskView()
        else:
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

    def sDataRepresentation(self):
        """
        :return:dict aller zur gui darstellung benötigten daten
        name, description, start, ende, priority, percentage, completed
        """
        dr = {"name":self.name, "description":self.description, "start": self.start, "ende": self.ende,
              "priority": self.priority, "percentage":self.sPercentage(), "completed":self.sCompleted,
              "masters_ende":self.sMastersEnde(), "masters_priority":self.sMastersPriority()}
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
        self.mappingsRecursivelyAcknowledgeTaskChange()

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
        clipbord_task.mappingsRecursivelyAcknowledgeTaskChange()
        self.sub_tasks.append(clipbord_task)

    def setMaster(self, task):
        self.master = task

    def addResultsFileAndDescription(self, file_path, short_description):
        self._results.append((file_path, short_description))


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
        if task is self._side_packed_project:
            task.delete()

        self.sub_tasks.remove(task)


    def isolatedTaskView(self, task):
        """
        isolate one task ond gives him the hole sheet space to look and work on
        :param task:
        """
        self._side_packed_project = self.sub_tasks
        task.setTaskManager(self)
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
            # print(f"y_index: {y_index}, y: {y}")
            for x_index, x in enumerate(y):
                # print(f"x_index: {x_index}, x: {x}")
                if isinstance(x, Task):
                    all_masters_strings_list = x.hierarchyTreePositionString()
                    actual_tasfile_typek = ">".join(all_masters_strings_list)
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
                # print(f"#09u09u recursive reset triggered in thread")
                [subtask.recursiveConditionalTimedeltaReset() for subtask in subtasks]

        self.renewal_thread = threading.Thread(target=renewal, args=(self.sub_tasks,), daemon=True)
        self.renewal_thread.start()



if __name__ == '__main__':
    one_task = Task(name="test_task")

