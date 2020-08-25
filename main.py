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
        self.last_file_path_depre = ""

        self.backend_queue = queue.Queue()
        self.back_end_thread = self._startBackEndThread()


        self.taskmanager = Taskmanager()
        self.mygtb = MyGuiToolbox()
        self.task_window_crator = TaskInputWindowCreator()
        self.task_frames_creator = TaskFrameCreator()
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

    @property
    def last_file_path(self):
        warnings.warn("last_file_path is deprecated with optipons_file_settings", DeprecationWarning)
        return self.last_file_path_depre

    @last_file_path.setter
    def last_file_path(self, value):
        warnings.warn("last_file_path is deprecated with options_file_settings", DeprecationWarning)
        self.last_file_path_depre = value

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

    def onCreateResult(self, task, event, values, command, *args, **kwargs):
        self.result_file_creator.newResultFile(task=task, kind_of_porogramm=command, result_path=self.opt.sUsedResultFolder())

    def onOptionButtonMenu(self, task, event, values, *args, **kwargs):
        """Method for Button menu command mapping"""
        print()
        try:
            self._executeBasicOptionButtonMenuCommands(values=values, event=event, task=task)
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
        file_path = tools.ensureFilePathExtension(file_path)
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

    def onEditTask(self, task, *args, **kwargs):
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
        y, x = [int(x) for x in coordinates.split()]
        return x, y

    def _executeCreatedFile(self, event, values):
        """Opens already existing task-result-file in system corresponding program like libre office or else """
        command = values[event]
        _, _, file_path = command.rpartition(" <-> ")
        if os.path.isfile(file_path):
            tools.openExternalFile(file_path=file_path#, threads=self._extern_threads
                                   )

    def _executeBasicOptionButtonMenuCommands(self, values, event, task):
        """executes the basic commands of the option Button menue"""
        command = values[event]
        action = self.sFunctionMapping()[command]
        action(task=task, values=values, command=command, event=event)

    def _userExit(self, event, window):
        """checks for and executes Exit if asked for"""
        if event in (inter.exit, None):
            self._stopBackEndThread()
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

        print(f"#29824 event: {event}, values: {values}")
        command, _, string_coordinates = event.partition("#7#")
        print(f"command: {command}, string_coordinates:{string_coordinates}, some string_co: {'True' if string_coordinates else 'False'}")

        if string_coordinates:
            self._executeCoordinateCommand(string_coordinates=string_coordinates, command=command,
                                           values= values, event=event)
        else:
            print(f"#iuihbjlksndfoij command: {command}")
            print(f"self.function mapping: {self.sFunctionMapping()}")
            action = self.sFunctionMapping()[command]
            print(f"#90920983 {action}")
            action()

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

    def _stopBackEndThread(self):
        self.backend_queue.put(("###breakbreakbreak###", None))

    def _autoSaveTC(self):
        print(f"#238923 in autosaveTQ")
        self.taskmanager.save(os.path.join("autosave", f"autosave-{tools.nowDateTime()}.tak"))

    def _autoSaveFileHandlingTC(self):
        print(f"#09u10 in _autosaveFileHandlinTQ")
        # todo function is finished, must be but in place, question is,
        #  shall i make many threads for every function like this or implement an single queue.get(block=True)
        #  controlled thread (bring autosave thread in here too than)
        if self.opt.autosave_handling:
            autosave_path = self.opt.sUsedAutosavePath()
            all_auto_save_files = os.listdir(autosave_path)
            all_auto_save_files.sort()
            all_file_paths = [os.path.join(autosave_path, file) for file in all_auto_save_files]

            if self.opt.sAutosaveAmountType() == inter.pieces:
                file_paths_for_deletion = all_file_paths[:-self.opt.sAutosaveAmount()]
                [(print(f"file will be deleted: {file}", end=""     )) for file in file_paths_for_deletion]
                print(f"all files: {len(all_auto_save_files)}, files for deletion {len(file_paths_for_deletion)}")
                # achtung [os.remove(file) for file in file_paths_for_deletion]
            else:
                timestamp = self._deltionTimeStamp(self.opt.sAutosaveAmount())
                file_paths_for_deletion = [file for file in all_file_paths if os.path.getmtime(file) < timestamp]
                [(print(f"file will be deleted: {file}")) for file in file_paths_for_deletion]
                print(f"all files: {len(all_auto_save_files)}, files for deletion {len(file_paths_for_deletion)}")

                # achtung [os.remove(file) for file in file_paths_for_deletion]

    # def autoSave(self):
    #     """perform auto save in a threat
    #     """
    #     thread = Thread(
    #             target=self.taskmanager.save,
    #             args=(os.path.join("autosave", f"autosave-{tools.nowDateTime()}.tak"),))
    #     thread.start()
    #     self.backend_threads.append(thread)

    def autoSave(self):
        """perform auto save in a threat
        """
        self.backend_queue.put((self._autoSaveTC, ()))
        self.backend_queue.put((self._autoSaveFileHandlingTC, ()))

    def _instantiateBasicFolderStructurTC(self, folders):
        print(f"#9028u30 in _instantiateFolderStructurTQ")
        for folder in folders:
            tools.createPathWithExistsCheck(path=folder)

    def _instantiateBasicFolderStructur(self, folders):
        self.backend_queue.put((self._instantiateBasicFolderStructurTC, folders))

    # todo did not work out to command sg.window from outside Thread but it is needed to work out this:
    #  invalid command name "140326498775872showtip"
    #      while executing
    #  "140326498775872showtip"
    #      ("after" script)
    #  error message its indicates that window gets closed before all ending-related-work is done

# def _bakendDelayedWindowCloseTC(self, sleep_time_and_window):
    #     sleep_time, window = sleep_time_and_window
    #     time.sleep(sleep_time)
    #     window.close()
    #
    # def _bakendDelayedWindowClose(self, sleep_time, window):
    #     self.backend_queue.put((self._bakendDelayedWindowCloseTC, (sleep_time, window)))

    def _startBackEndThread(self):
        thread = Thread(target=self._backEndThread, args=())
        thread.start()
        return thread

    def _backEndThread(self):
        while True:
            action, args = self.backend_queue.get(block=True)
            if args:
                print(f"#0293i action: {action}, args: {args}")
                action(args)
            else:
                if action == "###breakbreakbreak###":
                    break
                print(f"#013918 action: {action}")
                action()

    def mainLoop(self):
        """loop which is needed for event handling
        """
        while True:
            self.main_window = self.mainWindow()
            self.progbar.stop()
            event, values = self.main_window.read()
            print(F"#98765 event: {event}; vlues: {values}")

            self.executeEvent(event=event, window=self.main_window, values=values)
            self.window_size = self.main_window.size  # remember breaks down sometimes, why?!?
            self.window_location = self.main_window.current_location()
            self.progbar.start()
            self.main_window.close()

            self.autoSave()

    def __del__(self):
        self.progbar.kill()

if __name__ == '__main__':


    # debug_printer = DebugPrinter() #achtung removes all console output,
                                     #achtung despite its name its really bad for debuging while dev xD
    cwdBashFix()
    main_gui_task_atack = TaskAttack(base_file="base.tak")

# add short keys

# user defined folder structure dosent work as expected

# no troubleshooting if file path contains double //

#fixme file icon dont disapeare by deleting files

# todo maybe there is a way for print()/Error > stdout > DebugPrinter

# fixme if language gets changed in option menu and one press cancel

# todo beauty taskatack.last_file_path is deprecated with option.file_path_settings


# fixme task frame shows file existence even there is no file
# todo dev this fixme is an backend thread dev

# todo check for deleted or moved files,
#  file symbol once activated it never updates becouse
#  there is no check that updates task.results.list

# todo complet documentation and code cleanup

# todo insert links, implement it like results
# this todo is an todo dev

# todo make a reload progressbar

# todo dev make a Qt version

# todo think maybe make a sort of game out of this like get points for accomplished task etc



# remember beauty look out for chances to easily improve performance

# remember or later scroll position beibehalten (not possible as i know)

#remember or later gui_element.TaskFrameCreater._toolTipText
# date is shown yyyy-mm-dd 00:00:00 should i exclude the hours if its always zerro,
# or shouldnt i change it in case for later improvements whit exact time?!?
# as is write this down here i think i shouldnt

#todo window displays itself over result programm


