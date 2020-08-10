__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"

import copy
import itertools
import os
import sys
import threading
import time

import PySimpleGUI as sg

import gui_elements
import tools
from gui_elements import TaskInputWindowCreator, TaskFrameCreator, MyGuiToolbox
from internationalisation import inter
from task import Taskmanager, Task
from threading import Thread


class TaskAttack:
    def __init__(self):


        self.unsaved_project = False
        self.last_deleted_task:Task = None
        self.auto_save_thread:Thread = None
        self._clipboard:Task = None
        self._extern_threads = []
        self.last_file_path = ""

        self.taskmanager = Taskmanager()
        self.mygtb = MyGuiToolbox()
        self.task_window_crator = TaskInputWindowCreator()
        self.task_frames_creator = TaskFrameCreator()
        self.result_file_creator = gui_elements.ResultFileCreator()

        self.window_size = sg.Window.get_screen_size()
        self.window_location = (None, None)

        self.mainLoop()

    @staticmethod
    def sMenuBar():
        """
        :return: list of list: sg.Menu.layout
        """
        return inter.menu_bar

    @staticmethod
    def sTableDummy():
        """
        :return: table dummy needed on an empty sheet
        """
        return [sg.Text(text=inter.projects, size=(20, 20))]

    @staticmethod
    def onSetTaskAsCompleted(task, *args, **kwargs):
        task.changeCompleted()

    @staticmethod
    def onReload(*args, **kwargs):
        """does nothing so loop starts anew and matrix and window gets build anew"""
        pass

    def sLastUsedFolder(self):
        if self.last_file_path:
            return os.path.split(self.last_file_path)[0]

    def sFunctionMapping(self):
        """
        :return: function mapping for window/global executable functions
        """
        # correspondig lists:
        # inter.menu_bar
        # inter.b_b_m_l
        # inter.c_b_m_l
        #inter.chreate_result_menu

        return {#Globals:
                inter.new_project: self.onAddProject, inter.reload: self.onReload,
                inter.new_project_sheet: self.onNewFile, inter.open: self.onLoad, inter.save: self.onSave,
                inter.save_at: self.onSaveAt, inter.restore_task: self.onRestoreTask,

                #Locals:
                "bearb-": self.onEditTask, "subta-": self.onNewSubTask, "compl-": self.onSetTaskAsCompleted,
                "-BMENU-": self.onOptionButtonMenu,

                #ButtonCommands:
                inter.sub_task: self.onNewSubTask, inter.isolate: self.onIsolateTask, inter.edit: self.onEditTask,
                inter.delete: self.onDeleteTask, inter.paste: self.onInsertTask, inter.cut: self.onCutTask,
                inter.copy: self.onCopyTask, inter.tree_view: self.onTreeView,

                #Extern Programms
                inter.writer: self.onCreateResult, inter.spreadsheet: self.onCreateResult,
                inter.presentation:self.onCreateResult, inter.database: self.onCreateResult, inter.drawing:
                self.onCreateResult, inter.gimp: self.onCreateResult, inter.svg: self.onCreateResult,
                }

    def onCreateResult(self, task, event, values, command, *args, **kwargs):
        self.result_file_creator.newResultFile(task=task, kind_of_porogramm=command)

    def onOptionButtonMenu(self, task, event, values, *args, **kwargs):
        """Method for Button menu command mapping"""
        try:
            self._executeBasicOptionButtonMenuCommands(values=values, event=event, task=task)
        except KeyError:
            self._executeCreatedFile(event=event, values=values)

    def onLoad(self, *args, **kwargs):
        self.dataLossPrevention()
        file_path = sg.PopupGetFile(message=inter.open, initial_folder=self.sLastUsedFolder(),
                                    file_types=(("TaskAtack", "*.tak"),), keep_on_top=True)
        if file_path:
            self.last_file_path = file_path
            self.taskmanager.load(file_path)

    def onSaveAt(self, *args, **kwargs):
        self.unsaved_project = False
        file_path = sg.PopupGetFile(message=inter.save_at, save_as=True, file_types=(("TaskAtack", "*.tak"),),
                                    initial_folder=self.sLastUsedFolder(), keep_on_top=True, default_extension=".tak")
        file_path = tools.completeFilePathWithExtension(file_path)
        if file_path:
            self.last_file_path = file_path
            self.taskmanager.save(file_path)

    def onSave(self, *args, **kwargs):
        self.unsaved_project = False
        if self.last_file_path:
            self.taskmanager.save(self.last_file_path)
        else:
            self.onSaveAt()

    def onNewFile(self, *args, **kwargs):
        self.dataLossPrevention()
        self.taskmanager = Taskmanager()
        self.reset()

    def onAddProject(self, *args, **kwargs):
        event, values = self.task_window_crator.inputWindow(kind=inter.project, )
        print(F"#23442 event: {event}; vlues: {values}")

        if event in {inter.cancel, None}:
            return
        self.taskmanager.addSubTask(name=values['name'], description=values['description'], start=values['start'],
                                    end=values['ende'],
                                    priority=values['priority'])

    def onRestoreTask(self, *args, **kwargs):
        if self.last_deleted_task:
            self.last_deleted_task.recover()

    def onEditTask(self, task, *args, **kwargs):
        event, values = self.task_window_crator.inputWindow(**task.sDataRepresentation())
        print(F"#125456 event: {event}; vlues: {values}")
        if tools.eventIsNotNone(event):
            task.update(**values)

    def onNewSubTask(self, task, *args, **kwargs):
        event, values = self.task_window_crator.inputWindow(kind=inter.task, masters_ende=task.sEnde(), masters_priority=task.sPriority())
        print(F"#987453 event: {event}; vlues: {values}")
        if tools.eventIsNotNone(event):
            task.addSubTask(**values)

    def onIsolateTask(self, task, *args, **kwargs):
        self.task_frames_creator.changeMenuListToIsolated()
        self.taskmanager.isolatedTaskView(task)

    def onTreeView(self, task, *args, **kwargs):
        self.task_frames_creator.setBasichButtonMenuList()
        self.taskmanager.deisolateTaskView(task)

    def onDeleteTask(self, task, *args, **kwargs):
        if self.mygtb.YesNoPopup(title=inter.delete, text=inter.realy_delete):
            self.last_deleted_task = task
            task.delete()

    def onCutTask(self, task, *args, **kwargs):
        self._clipboard = task
        task.delete()

    def onCopyTask(self, task, *args, **kwargs):
        self._clipboard = task

    def onInsertTask(self, task, *args, **kwargs):
        hard_copy = copy.deepcopy(self._clipboard)
        hard_copy.setMaster(task)
        task.insertClipbordTask(clipbord_task=hard_copy)

    @staticmethod
    def _getCoordinatesAsInts(coordinates):
        """strips button event down to button coordinates
        :return: button matrix coordinates
        """
        coordinates = coordinates.replace("(", "")
        coordinates = coordinates.replace(")", "")
        coordinates = coordinates.replace(",", "")
        y, x = [int(x) for x in coordinates.split()]
        return x, y

    def _executeCreatedFile(self, event, values):
        """Opens already existing task-result-file in system corresponding program like libre office or else """
        command = values[event]
        _, _, file_path = command.rpartition(" <-> ")
        if os.path.isfile(file_path):
            tools.startExternAplicationThread(file_path=file_path, threads=self._extern_threads)

    def _executeBasicOptionButtonMenuCommands(self, values, event, task):
        """executes the basic commands of the option Button menue"""
        command = values[event]
        action = self.sFunctionMapping()[command]
        action(task=task, values=values, command=command, event=event)


    def _userExit(self, event, window):
        """checks for and executes Exit if asked for"""
        if event in (inter.exit, None):
            self.dataLossPrevention()
            window.close()
            sys.exit(0)

    def _setDataLossPreventionStatus(self, event):
        """looks for user action and sets flag for not saved question, if new data is created"""
        if event not in (inter.new_project_sheet, inter.open, inter.save, inter.save_at,
                         inter.exit, inter.reload, inter.help, inter.about, None):
            self.unsaved_project = True

    def _executeCoordinateCommand(self, string_coordinates:str, command:str, values:dict, event:str):
        """
        executes Task specific commands, which alters with every task
        :param string_coordinates: task matrix coordinates
        """
        int_coordinates = self._getCoordinatesAsInts(string_coordinates)
        task = self.getTaskFromMatrix(coordinates=int_coordinates)
        action = self.sFunctionMapping()[command]
        action(task=task, values=values, event=event, command=command)

    def executeEvent(self, event, window, values, *args, **kwargs):
        """takes event, values and window and executes corresponding action from command-mapping
        :param event: user_event
        :param window: TaskAttack-window
        :param values: dict sg.values
        """
        self._userExit(event=event, window=window)
        self._setDataLossPreventionStatus(event)

        command, _, string_coordinates = event.partition("#7#")
        print(f"command: {command}, string_coordinates:{string_coordinates}")

        if string_coordinates:
            self._executeCoordinateCommand(string_coordinates=string_coordinates, command=command,
                                           values= values, event=event)
        else:
            action = self.sFunctionMapping()[command]
            action()

    def dataLossPrevention(self):
        """checks if there is an open unsaved file and asks for wish to save
        """
        if self.unsaved_project:
            if self.mygtb.YesNoPopup(title=inter.open_project, text=f"{inter.save}?"):
                self.onSaveAt()

    def autoSave(self):
        """perform auto save in a threat, creates 10 different files
        """
        while self.auto_save_thread and self.auto_save_thread.is_alive():
            time.sleep(2)
        self.auto_save_thread = threading.Thread(
                target=self.taskmanager.save,
                args=(os.path.join("autosave", f"autosave-{tools.nowDateTime()}.tak"),))
        self.auto_save_thread.start()

    def reset(self):
        """tasks to perform if task manager has to reset/start anew
        """
        self.last_file_path = ""
        self.unsaved_project = False

    def createProjectsLayout(self):
        """creates layout list_of_list and fills it with destinct FRAMES
        :return: list of list, containig showable SG-FRAMES
        """
        orginal_display_matrix = self.taskmanager.displayMatrix()
        base_layout = copy.deepcopy(orginal_display_matrix)

        for y_index, y in enumerate(orginal_display_matrix):
            for x_index, element in enumerate(y):
                if isinstance(element, Task):
                    frame_here = self.task_frames_creator.taskFrame(element)
                    base_layout[y_index][x_index] = frame_here
                else:
                    frame_here = self.task_frames_creator.emptyTaskFrame()
                    base_layout[y_index][x_index] = frame_here
        return base_layout

    def getTaskFromMatrix(self, coordinates):
        """
        :param coordinates: tuple(int, int)
        :return: destinct task from matric
        """
        task_matrix = self.taskmanager.sTaskMatrix()
        return task_matrix[coordinates[0]][coordinates[1]]

    def propperWindowLayout(self, menu_bar, project_matrix):
        """creates tree layout either with project_matrix if available, or with a table dummy
        :return: finished layout ready for displaying
        """
        if len(project_matrix) == 1 and isinstance(project_matrix[0][0], sg.Text):
            layout = [[sg.MenuBar(menu_bar, size=(40, 40))], *project_matrix]
        else:
            collumn = sg.Column(project_matrix, scrollable=True, size=self.window_size)
            layout = [[sg.MenuBar(menu_bar), collumn]]
        return layout

    def projectMatrixOneFieldBigger(self, project_table):
        """
        :param project_table: list of lists task frames
        :return: list of lists task frames one bit bigger so tooltip wont show out of screensize
        """
        try:
            project_table[0].append(self.task_frames_creator.emptyTaskFrame())
            project_table.append([self.task_frames_creator.emptyTaskFrame()])
        except AttributeError:
            pass
        return project_table

    def propperProjectMatrix(self):
        """
        :return: either table_dummy if no project available, or propper project table
        """
        project_table = self.createProjectsLayout()
        flat = list(itertools.chain.from_iterable(project_table))
        if not flat:
            project_table = [self.sTableDummy()]
        else:
            project_table = self.projectMatrixOneFieldBigger(project_table)

        return project_table

    def mainWindow(self):
        """creates main window
        :return: main window
        """
        project_matrix = self.propperProjectMatrix()
        #tools.printMatrix("#333", project_matrix)
        layout = self.propperWindowLayout(self.sMenuBar(), project_matrix)
        main_window = sg.Window(title=inter.app_name, layout=layout,
                                finalize=True, resizable=True, size=self.window_size, location=self.window_location)
        return main_window

    def mainLoop(self):
        """loop which is needed for event handling
        """
        while True:
            main_window = self.mainWindow()
            event, values = main_window.read()
            print(F"#98765 event: {event}; vlues: {values}")

            # print(f"mainloop: event: {event}, values: {values}")
            self.executeEvent(event=event, window=main_window, values=values)
            self.window_size = main_window.size  # remember breaks down sometimes, why?!?
            self.window_location = main_window.current_location()
            main_window.close()
            self.autoSave()


if __name__ == '__main__':
    main_gui_task_atack = TaskAttack()

# todo dev implement data creation by outside programs like writer, gimp, etc
#  additional to that there have to be a save_file library and mapping

# todo complet documentation and code cleanup

# todo beauty --> uniform task and taskmanager

# remember beauty look out for chances to easily improve performance

# remember or later scroll position beibehalten (not possible as i know)

#remember or later gui_element.TaskFrameCreater._toolTipText
# date is shown yyyy-mm-dd 00:00:00 should i exclude the hours if its always zerro,
# or shouldnt i change it in case for later improvements whit exact time?!?
# as is write this down here i think i shouldnt

# todo folder creation in documents
# todo ad a little file sing to task frame to indicate existence of results

# todo dev make a Qt version




