__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"

import copy
import itertools
import os
import queue
import sys
import time
import warnings
from datetime import timedelta
from threading import Thread

import PySimpleGUI as sg
from colorama import Fore

import gui_elements
import tools
from gui_elements import TaskInputWindowCreator, TaskFrameCreator, MyGuiToolbox, Progressbar
from internationalisation import inter
from option import Option
from task import Taskmanager, Task
from tools import cwdBashFix, nowDateTime


class TaskAttack:
    def __init__(self, base_file:str=None):


        self.opt = Option("user_setup.ats")

        self.unsaved_project = False
        self.last_deleted_task:Task = None
        #self.auto_save_thread:Thread = None #now ther will be more worker threads in the back so this changes
        self._clipboard:Task = None
        self._extern_threads = []
        self.last_file_path = base_file if base_file else ""

        self.background_queue = queue.Queue()
        self.back_end_thread = self._startBackGroundThread()


        self.taskmanager = Taskmanager()
        self.mygtb = MyGuiToolbox()
        self.task_window_crator = TaskInputWindowCreator()
        #todo this time would be unnessasary
        # self.task_frames_creator = TaskFrameCreator()
        self.result_file_creator = gui_elements.ResultFileCreator()
        self.progbar = Progressbar(type_here="blue_dotted_ring")

        self.window_size = sg.Window.get_screen_size()
        self.window_location = (None, None)

        if base_file:
            try:
                self.taskmanager.load(base_file)
            except:
                pass
        self._instantiateBasicFolderStructur(
                folders=(self.opt.sUsedMainFolder(), self.opt.sUsedResultFolder(), self.opt.sUsedAutosavePath()))
        self.mainLoop()

    #     #todo make a base file in option
    # @property
    # def last_file_path(self):
    #     #warnings.warn("last_file_path is deprecated with optipons_file_settings", DeprecationWarning)
    #     return self.last_file_path_depre
    #
    # @last_file_path.setter
    # def last_file_path(self, value):
    #     #warnings.warn("last_file_path is deprecated with options_file_settings", DeprecationWarning)
    #     self.last_file_path_depre = value

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
        # inter.chreate_result_menu

        return {#Globals:
                inter.new_project: self.onAddProject, inter.reload: self.onReload,
                inter.new_project_sheet: self.onNewFile, inter.open: self.onLoad, inter.save: self.onSave,
                inter.save_at: self.onSaveAt, inter.restore_task: self.onRestoreTask,
                inter.settings: self.onGlobalOptions,

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

    def sRenewalNeedingFunctions(self):
        """
        all functions that needs an new window to display changes
        :return:
        """
        return {inter.new_project, inter.reload, inter.new_project_sheet, inter.open, inter.restore_task,
                inter.settings, "subta-", "compl-", #"-BMENU-",
                inter.sub_task, inter.isolate,inter.delete,
                inter.paste, inter.cut, inter.tree_view, }

    def onCreateResult(self, task, event, values, command, *args, **kwargs):
        self.result_file_creator.newResultFile(task=task, kind_of_porogramm=command, result_path=self.opt.sUsedResultFolder())

    def onOptionButtonMenu(self, task, event, values, *args, **kwargs):
        """Method for Button menu command mapping
        :return if executed command is one thats needs renewal of window"""
        try:
            return self._executeBasicOptionButtonMenuCommands(values=values, event=event, task=task)

        except KeyError as e:
            print(f"No Problem ERROR #34ehtrfh --> war kein basic option button command {e.__traceback__.tb_lineno}, {repr(e.__traceback__)}, {repr(e)},  {e.__cause__}")
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
        if file_path:
            file_path = tools.path.ensureFilePathExtension(file_path)
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
        print(f"#89721kjn")
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

    def onEditTask(self, task,  *args, **kwargs):
        # raise TypeError
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
            print(f"#092u03 in delete on Task")
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

    def onGlobalOptions(self, *args, **kwargs):
        self.opt.getSettingsFromUser()

    @staticmethod
    def _getCoordinatesAsInts(coordinates):
        """strips button event down to button coordinates
        :return: button matrix coordinates
        """
        coordinates = coordinates.replace("(", "")
        coordinates = coordinates.replace(")", "")
        coordinates = coordinates.replace(",", "")
        x, y = [int(xr) for xr in coordinates.split()]
        return x, y

    def _executeCreatedFile(self, event, values):
        """Opens already existing task-result-file in system corresponding program like libre office or else """
        command = values[event]
        _, _, file_path = command.rpartition(" <-> ")
        if os.path.isfile(file_path):
            tools.openExternalFile(file_path=file_path#, threads=self._extern_threads
                                   )

    def _executeBasicOptionButtonMenuCommands(self, values, event, task):
        """executes the basic commands of the option Button menue
        :return if executed command is one thats needs renewal of window"""
        command = values[event]
        action = self.sFunctionMapping()[command]
        action(task=task, values=values, command=command, event=event)
        return command in self.sRenewalNeedingFunctions()

    def _ifUserExit(self, event, window):
        """checks for and executes Exit if asked for"""
        if event in (inter.exit, None):
            self._stopBackGroundThread()
            self.dataLossPrevention()
            window.close()
            sys.exit(0)

    def _setDataLossPreventionFlag(self, event):
        """looks for user action and sets flag for not saved question, if new data is created"""
        if event not in (inter.new_project_sheet, inter.open, inter.save, inter.save_at,
                         inter.exit, inter.reload, inter.help, inter.about, None):
            self.unsaved_project = True

    def _executeCoordinateCommand(self, string_coordinates:str, command:str, values:dict, event:str):
        """
        executes Task specific commands, which alters with every task
        :param string_coordinates: task matrix coordinates
        :returns tuple: 1st window_renewal_flag: boolean, 2nd either task coordinates, or none if no coordinate
        """
        int_coordinates = self._getCoordinatesAsInts(string_coordinates)
        task = self.getTaskFromMatrix(coordinates=int_coordinates)
        action = self.sFunctionMapping()[command]
        return action(task=task, values=values, event=event, command=command) or command in self.sRenewalNeedingFunctions(), int_coordinates

    def executeEvent(self, event, window, values, *args, **kwargs):
        """takes event, values and window and executes corresponding action from command-mapping
        :param event: user_event
        :param window: TaskAttack-window
        :param values: dict sg.values
        :returns tuple: 1st window_renewal_flag: boolean, 2nd either task coordinates, or none if no coordinate
        """
        self._ifUserExit(event=event, window=window)
        self._setDataLossPreventionFlag(event)

        command, _, string_coordinates = event.partition("#7#")

        if string_coordinates:
            return self._executeCoordinateCommand(string_coordinates=string_coordinates, command=command,
                                           values= values, event=event)
        else:
            action = self.sFunctionMapping()[command]
            action()
            return command in self.sRenewalNeedingFunctions(), None

    def dataLossPrevention(self):
        """checks if there is an open unsaved file and asks for wish to save
        """
        if self.unsaved_project:
            if self.mygtb.YesNoPopup(title=inter.open_project, text=f"{inter.save}?"):
                self.onSaveAt()

    def _deltionTimeStamp(self, autosave_amount):
        now_time = nowDateTime()
        whished_time = now_time - timedelta(days=autosave_amount)
        timestamp = time.mktime(whished_time.timetuple())
        return timestamp

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
                    frame_here = gui_elements.TaskFrame(task=element)
                    base_layout[y_index][x_index] = frame_here
        return base_layout

    def getTaskFromMatrix(self, coordinates):
        """
        :param coordinates: tuple(int, int)
        :return: destinct task from matric
        """
        task_matrix = self.taskmanager.sTaskMatrix()
        return task_matrix[coordinates[1]][coordinates[0]]

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
            project_table[0].append(gui_elements.TaskFrame(None))
            project_table.append([gui_elements.TaskFrame(None)])
        except AttributeError as e:
            print(f"{Fore.RED}ERROR #08029i233 --> {e.__traceback__.tb_lineno}, {repr(e.__traceback__)}, {repr(e)},  {e.__cause__}{Fore.RESET}")

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

    def _stopBackGroundThread(self):
        """sends break command which causes while loop to exit"""
        self.background_queue.put(("###breakbreakbreak###", None))

    def _autoSaveTC(self, *args, **kwargs): #TC: Thread Command
        """performs auto save in background"""
        self.taskmanager.save(os.path.join(self.opt.sUsedAutosavePath(), f"autosave-{tools.nowDateTime()}.tak"))

    def _autoSaveFileHandlingTC(self, *args, **kwargs):
        """deletes auto save files to users settings""" #achtung
        if self.opt.autosave_handling:
            autosave_path = self.opt.sUsedAutosavePath()
            all_auto_save_files = os.listdir(autosave_path)
            all_auto_save_files.sort()
            all_file_paths = [os.path.join(autosave_path, file) for file in all_auto_save_files]

            if self.opt.sAutosaveAmountType() == inter.pieces:
                file_paths_for_deletion = all_file_paths[:-self.opt.sAutosaveAmount()]
                [os.remove(file) for file in file_paths_for_deletion] #achtung
            elif self.opt.sAutosaveAmountType() == inter.days:
                timestamp = self._deltionTimeStamp(self.opt.sAutosaveAmount())
                file_paths_for_deletion = [file for file in all_file_paths if os.path.getmtime(file) < timestamp]
                [os.remove(file) for file in file_paths_for_deletion] #achtung

    def autoSave(self):
        """perform auto save in a threat
        """
        self.background_queue.put((self._autoSaveTC, ()))
        self.background_queue.put((self._autoSaveFileHandlingTC, ()))

    def _instantiateBasicFolderStructurTC(self, folders, *args, **kwargs):
        print(f"#9028u30 in _instantiateFolderStructurTQ")
        for folder in folders:
            tools.path.ensurePathExists(path_here=folder)

    def _instantiateBasicFolderStructur(self, folders):
        self.background_queue.put((self._instantiateBasicFolderStructurTC, folders))

    def _startBackGroundThread(self):
        thread = Thread(target=self._backGroundThread, args=())
        thread.start()
        return thread

    def _backGroundThread(self):
        """executes commands in the background"""
        while True:
            action, args = self.background_queue.get(block=True)
            if action == "###breakbreakbreak###":
                break
            else:
                print(f"#0293i action: {action}, args: {args}")
                action(args)

    def mainLoop(self):
        """loop which is needed for event handling
        """
        window_renewal_flag = True
        while True:
            if window_renewal_flag:
                self.main_window = self.mainWindow()
            self.progbar.stop()
            event, values = self.main_window.read()
            window_renewal_flag, int_coordinates = self.executeEvent(event=event, window=self.main_window, values=values)
            print(f"#ß02i3ß0 event: {event}; window must be renewed: {window_renewal_flag}, frame cords to update: {int_coordinates}")
            if window_renewal_flag:
                self.window_size = self.main_window.size  # remember breaks down sometimes, why?!?
                self.window_location = self.main_window.current_location()
                self.progbar.start()
                self.main_window.close()
            else:
                if int_coordinates:
                    print(f"#902893 key to update: {f'-MY-TASK-FRAME-{str(int_coordinates)}'}")
                    self.main_window[f"-MY-TASK-FRAME-{str(int_coordinates)}"].Update(self.main_window)

            self.autoSave()

    def __del__(self):
        self.progbar.kill()
        self._stopBackGroundThread()

if __name__ == '__main__':


    # debug_printer = DebugPrinter() #achtung removes all console output,
                                     #achtung despite its name its really bad for debuging while dev xD
    tools.path.cwdBashFix()
    main_gui_task_atack = TaskAttack(base_file="base.tak")

# todo this still troubles once in a while
#  invalid command name "140326498775872showtip"
#      while executing
#  "140326498775872showtip"
#      ("after" script)
#  error message its indicates that window gets closed before all ending-related-work is done


# todo next add short keys --> before short keys there must be distinguished between update and reload

# todo make update or reload decision. i.e. load, save, etc. dont need new window, not even an update,
#  so there is potential for easy improvement

# todo set RadioRow in Place, instead of horizontal decision function !!!ACHTUNG first search for all kex appearances etc.

# todo maybe there is a way for print()/Error > stdout > DebugPrinter

# todo complet documentation and code cleanup

# todo dev insert links, implement it like results

# todo dev make a Qt version

# todo think maybe make a sort of game out of this like get points for accomplished task etc

# remember beauty look out for chances to easily improve performance

# remember or later scroll position beibehalten (not possible as i know)

#remember or later gui_element.TaskFrameCreater._toolTipText
# date is shown yyyy-mm-dd 00:00:00 should i exclude the hours if its always zerro,
# or shouldnt i change it in case for later improvements whit exact time?!?
# as is write this down here i think i shouldnt

#todo window displays itself over result programm

