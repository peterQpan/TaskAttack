__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"

import copy
import itertools
import os
import sys
import threading
import time

import gui_elements, tools
from gui_elements import TaskInputWindowCreator, TaskFrameCreator
from task import Taskmanager, Task
import PySimpleGUI as sg


class TaskAttack:
    def __init__(self):

        self.last_deleted_task = None
        self.taskmanager = Taskmanager()
        self.task_window_crator = TaskInputWindowCreator()
        self.task_frames_creator = TaskFrameCreator()

        self.unsaved_project = False
        self.auto_save_thread = None
        self.last_file_path = ""

        self.window_size = sg.Window.get_screen_size()
        self.window_location = (None, None)

        self.mainLoop()

    @staticmethod
    def sMenuBar():
        return (['Datei', ['Neue Projekt Tabelle', 'Öffnen', 'Speichern', 'Speichern unter', 'Exit']],
                ['Projekt', ['Neues Projekt']],
                ['Bearbeiten', ['Widerherstellen']],
                ['Fenster', ['Reload']],
                ['Hilfe', 'Über...'])

    @staticmethod
    def sTableDummy():
        return [sg.Text(text="Projekts", size=(20, 20))]

    def sLastUsedFolder(self):
        if self.last_file_path:
            return os.path.split(self.last_file_path)[0]

    def sFunctionMapping(self):
        """
        :return: function mapping for window/global executable functions
        """
        #todo beauty can i avoid redundance with _buttonMenuList() und this dict?!?
        return {#Globals:
                "Neues Projekt": self.onAddProject, "Reload": self.onReload,
                "Neue Projekt Tabelle": self.onNewFile, "Öffnen": self.onLoad, "Speichern": self.onSave,
                "Speichern unter": self.onSaveAt, "Widerherstellen": self.onRecoverDeletedTask,

                #Locals:
                "bearb-": self.onWorkOnTask, "subta-": self.onNewSubTask, "compl-": self.onSetTaskAsCompleted,
                "-BMENU-": self.onOptionButtonMenu,

                #ButtonCommands:
                "Unteraufgabe": self.onNewSubTask, "Isolieren": self.onIsolateTask, "Bearbeiten": self.onWorkOnTask,
                "Löschen": self.onDeleteTask, "Einfügen": self.onInsertTask, "Ausschneiden": self.onCutTask, "Kopieren": self.onCopyTask
                }

    def onOptionButtonMenu(self, task, event, values, *args, **kwargs):
        """Method for Button menu command mapping"""
        command = values[event]
        action = self.sFunctionMapping()[command]
        action(task)

    def onLoad(self, *args, **kwargs):
        self.dataLossPrevention()
        file_path = sg.PopupGetFile("Öffnen", initial_folder=self.sLastUsedFolder(),
                                    file_types=(("TaskAtack", "*.tak"),), keep_on_top=True)
        if file_path:
            self.last_file_path = file_path
            self.taskmanager.load(file_path)

    def onSaveAt(self, *args, **kwargs):
        self.unsaved_project = False
        file_path = sg.PopupGetFile("Speichern in", save_as=True, file_types=(("TaskAtack", "*.tak"),),
                                    initial_folder=self.sLastUsedFolder(), keep_on_top=True, default_extension=".tak")
        file_path = self._completeFilePathWithExtension(file_path)
        if file_path:
            self.last_file_path = file_path
            self.taskmanager.save(file_path)

    def onSave(self, *args, **kwargs):
        self.unsaved_project = False
        if self.last_file_path:
            self.taskmanager.save(self.last_file_path)
        else:
            self.onSaveAt()

    def onReload(self, *args, **kwargs):
        """does nothing so loop starts anew and matrix and window gets build anew"""
        pass

    def onNewFile(self, *args, **kwargs):
        self.dataLossPrevention()
        self.taskmanager = Taskmanager()
        self.reset()

    def onAddProject(self, *args, **kwargs):
        event, values = self.task_window_crator.inputWindow(kind="Projekt", )
        if event in {"Abbrechen", None}:
            return
        self.taskmanager.addProject(name=values['name'], description=values['description'], start=values['start'],
                                    end=values['ende'],
                                    priority=values['priority'])

    def onRecoverDeletedTask(self, *args, **kwargs):
        if self.last_deleted_task:
            self.last_deleted_task.recover()

    def onWorkOnTask(self, task, *args, **kwargs):
        event, values = self.task_window_crator.inputWindow(**task.sDataRepresentation())
        if self._eventIsNotNone(event):
            task.update(**values)

    def onNewSubTask(self, task, *args, **kwargs):
        event, values = self.task_window_crator.inputWindow(kind="Aufgabe", masters_ende=task.sEnde())
        if self._eventIsNotNone(event):
            task.addSubTask(**values)

    def onSetTaskAsCompleted(self, task, *args, **kwargs):
        task.changeCompleted()

    def onIsolateTask(self):
        # todo dev isolated task tree view
        pass

    def onDeleteTask(self, task, *args, **kwargs):
        if gui_elements.YesNoPopup(title="Löschen", text="Wirklich löschen"):
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

    def _userExit(self, event, window):
        """checks for and executes Exit if asked for"""
        if event in ("Exit", None):
            self.dataLossPrevention()
            window.close()
            sys.exit(0)

    def _setDataLossPreventionStatus(self, event):
        if event not in ('Neue Projekt Tabelle', 'Öffnen', 'Speichern', 'Speichern unter',
                         'Exit', 'Reload', 'Hilfe', 'Über...', None):
            self.unsaved_project = True

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

    def executeEvent(self, event, window, values, *args, **kwargs):
        self._userExit(event=event, window=window)
        self._setDataLossPreventionStatus(event)

        command, _, string_coordinates = event.partition("#7#")
        print(f"command: {command}, string_coordinates:{string_coordinates}")

        if string_coordinates:
            int_coordinates = self._getCoordinatesAsInts(string_coordinates)
            task = self.getTaskFromMatrix(coordinates=int_coordinates)
            action = self.sFunctionMapping()[command]
            action(task=task, values=values, event=event)
        else:
            action = self.sFunctionMapping()[command]
            action()

    def _completeFilePathWithExtension(self, file_path):
        """
        checks file path for ".atk" extension and adds it if necessary
        :param file_path: "file_path_string"
        :return: "some "file_path_string.tak"
        """
        file_name, extension = os.path.splitext(file_path)
        if not extension:
            file_path += ".tak"
        return file_path

    def dataLossPrevention(self):
        """checks if there is an open unsaved file and asks for wish to save
        """
        if self.unsaved_project:
            if gui_elements.YesNoPopup(title="Offenes Projekt", text="Speichern?"):
                self.onSaveAt()

    def autoSave(self):
        """perform auto save in a threat, creates 10 different files
        """
        while self.auto_save_thread and self.auto_save_thread.is_alive():
            time.sleep(2)
        self.auto_save_thread = threading.Thread(target=self.taskmanager.save,
                                                 args=(
                                                     os.path.join("autosave", f"autosave-{tools.nowDateTime()}.tak"),))
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

        # todo beauty --->
        #  delete out commented on 2020-08-04
        for y_index, y in enumerate(orginal_display_matrix):
            for x_index, element in enumerate(y):
                if isinstance(element, Task):
                    frame_here = self.task_frames_creator.taskFrame(element)
                    base_layout[y_index][x_index] = frame_here
                else:# isinstance(element, str):
                    frame_here = self.task_frames_creator.emptyTaskFrame()
                    base_layout[y_index][x_index] = frame_here
                # else:
                #     raise RuntimeError("irgend etwas vergessen!!!!")
        return base_layout

    def getTaskFromMatrix(self, coordinates):
        """
        :param coordinates: tuple(int, int)
        :return: destinct task from matric
        """
        task_matrix = self.taskmanager.sTaskMatrix()
        return task_matrix[coordinates[0]][coordinates[1]]

    @staticmethod
    def _eventIsNotNone(event):
        """checks event for None, Abbrechen
        :param event: sg.window.read()[0]
        :return: true if not close or Abrechen
        """
        if event and event != "Abbrechen":
            return True
        return False

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
        tools.printMatrix("#333", project_matrix)
        layout = self.propperWindowLayout(self.sMenuBar(), project_matrix)
        main_window = sg.Window('TaskAtack Project and Taskmanager', layout,
                                finalize=True, resizable=True, size=self.window_size, location=self.window_location)
        return main_window

    def mainLoop(self):
        """loop which is needed for event handling
        """
        while True:
            main_window = self.mainWindow()
            event, values = main_window.read()
            print(f"mainloop: event: {event}, values: {values}")
            self.executeEvent(event=event, window=main_window, values=values)
            self.window_size = main_window.size  # todo breaks down sometimes, why?!?
            self.window_location = main_window.current_location()
            main_window.close()
            self.autoSave()



# todo complet documentation and code cleanup


if __name__ == '__main__':
    main_gui_task_atack = TaskAttack()



# todo dev isolate view von tasks

# todo scroll position beibehalten (not possible as i know)

# todo beauty look out for chances to easily improve performance

# todo beauty --> uniform task and taskmanager

## todo figure colorcheme someday task, full deadline, etc

## todo beauty option button has no relief

# todo beauty clear language interface either german OR english not a little bit of both --> todo dev language and translating class

