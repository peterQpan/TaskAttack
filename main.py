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

from tools import printMatrix


class TaskAttack:
    def __init__(self):

        self.taskmanager = Taskmanager()
        self.task_window_crator = TaskInputWindowCreator()
        self.task_frames_creator = TaskFrameCreator()

        self.unsaved_project = False
        self.auto_save_thread = None
        self.last_file_path = ""

        self.window_size = sg.Window.get_screen_size()
        self.window_location = (None,None)

        self.mainLoop()

    @staticmethod
    def sMenuBar():
        return (['Datei', ['Neue Projekt Tabelle', 'Öffnen', 'Speichern', 'Speichern unter', 'Exit']],
                ['Projekt', ['Neues Projekt']], ['Fenster', ['Reload']],
                ['Hilfe', 'Über...'])

    @staticmethod
    def sTableDummy():
        return [sg.Text(text="Projekts", size=(20, 20))]

    def sGlobalFunctionMapping(self):
        """
        :return: function mapping for window/global executable functions
        """
        return {"Neues Projekt": self.onAddProject, None: self.onQuit, "Exit": self.onQuit, "Reload":self.onReload,
                "Neue Projekt Tabelle":self.onNewFile, "Öffnen": self.onLoad, "Speichern": self.onSave,
                "Speichern unter":self.onSaveAt}

    def sLocalCommandMapping(self):
        """
        :return: function mapping for local/taskspecivic functions wich corespondents to x,y tasc koordinates
        """
        return {"bearb-": self.onWorkOnTask, "subta-": self.onNewSubTask, "compl-":self.onSetTaskAsCompleted}

    def sLastUsedFolder(self):
        if self.last_file_path:
            return os.path.split(self.last_file_path)[0]

    def onQuit(self, window, *args, **kwargs):
        self.dataLossPrevention()
        window.close()
        sys.exit(0)

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
                                    initial_folder=self.sLastUsedFolder(), keep_on_top=True)
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

    def onWorkOnTask(self, event, *args, **kwargs):
        task = self.getTaskFromMatrix(event)
        task: Task
        event, values = self.task_window_crator.inputWindow(**task.sDataRepresentation(), existend=True)
        print(f"#902389090 event: {event}, values: {values}")
        if event == "Löschen":
            task.delete()
        elif self._eventIsNotNone(event):
            task.update(**values)

    def onAddProject(self, *args, **kwargs):
        event, values = self.task_window_crator.inputWindow(kind="Projekt", )
        if event in {"Abbrechen", None}:
            return
        print(values)
        self.taskmanager.addProject(name=values['name'], description=values['description'], start=values['start'],
                                    end=values['ende'],
                                    priority=values['priority'])

    def onNewSubTask(self, event, *args, **kwargs):
        task = self.getTaskFromMatrix(event)
        event, values = self.task_window_crator.inputWindow(kind="Aufgabe", masters_ende=task.sEnde())
        print(f"newSubtask #1983928kjndsa event: {event}, values: {values}")
        if self._eventIsNotNone(event):
            task.addSubTask(**values)

    def onSetTaskAsCompleted(self, event, *args, **kwargs):
        task = self.getTaskFromMatrix(event)
        task.changeCompleted()

    def dataLossPrevention(self):
        """checks if there is an open unsaved file and asks for wish to save
        """
        if self.unsaved_project:
            if gui_elements.OkCancelPopup(title="Offenes Projekt", text="Speichern?"):
                self.onSaveAt()

    def autoSave(self):
        """perform auto save in a threat, creates 10 different files
        """
        while self.auto_save_thread and self.auto_save_thread.is_alive():
            print("autosave_loop")
            time.sleep(2)
        self.auto_save_thread = threading.Thread(target=self.taskmanager.save,
                                                 args=(os.path.join("autosave", f"autosave-{tools.nowDateTime()}.tak"),))
        self.auto_save_thread.start()
        print("autosaved")

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
        printMatrix("orginal matrix:", orginal_display_matrix)
        base_layout = copy.deepcopy(orginal_display_matrix)

        # todo more modularisation here?!?
        for y_index, y in enumerate(orginal_display_matrix):
            for x_index, element in enumerate(y):
                if not element:
                    frame_here = self.task_frames_creator.emptyTaskFrame()
                    print(f"no element frame: {frame_here}")
                    printMatrix(f"#09i1uijn", base_layout)
                    base_layout[y_index][x_index] = frame_here
                    printMatrix(f"#25tgsr", base_layout)
                elif isinstance(element, Task):
                    frame_here = self.task_frames_creator.taskFrame(element)
                    print(f"task element frame: {frame_here}")
                    printMatrix(f"#68tiujfg", base_layout)
                    base_layout[y_index][x_index] = frame_here
                    printMatrix(f"#mhn656", base_layout)
                elif isinstance(element, str):
                    frame_here = self.task_frames_creator.emptyTaskFrame()
                    print(f"string frame: {frame_here}")
                    printMatrix(f"#bdsf42343", base_layout)
                    base_layout[y_index][x_index] = frame_here
                    printMatrix(f"#asdf344", base_layout)
                else:
                    raise RuntimeError("irgend etwas vergessen!!!!")
        return base_layout

    def executeEvent(self, event, window):
        """executes main window button clicks, by mapping it to two different, function_mapping_dicts"""
        if event not in ('Neue Projekt Tabelle', 'Öffnen', 'Speichern', 'Speichern unter',
                         'Exit', 'Reload', 'Hilfe', 'Über...'):
            self.unsaved_project = True
        try:
            action = self.sGlobalFunctionMapping()[event]
        except KeyError:
            action = self.sLocalCommandMapping()[event[:6]]
        action(event=event, window=window, values=0)

    def getTaskFromMatrix(self, event):
        """splits button-coordinate from event and returns coresponding task
        :param event: type: sg.window.read()[0]
        :return: destinct task from matric
        """
        coordinates = self._getCoordinates(event)
        task_matrix = self.taskmanager. sTaskMatrix()
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

    @staticmethod
    def _getCoordinates(event):
        """strips button event down to button coordinates
        :return: button matrix coordinates
        """
        _, _, rest = event.partition("(")
        rest = rest.replace(")", "")
        rest = rest.replace(",", "")
        y, x = [int(x) for x in rest.split()]
        return x, y

    def propperWindowLayout(self, menu_bar, project_matrix):
        """creates tree layout either with project_matrix if available, or with a table dummy
        :return: finished layout ready for displaying
        """
        if len(project_matrix) == 1 and isinstance(project_matrix[0][0], sg.Text):
            layout = [[sg.MenuBar(menu_bar, size=(40, 40))], *project_matrix]
        else:
            collumn = sg.Column(project_matrix, scrollable=True, size=self.window_size)
            layout = [[sg.MenuBar(menu_bar), collumn]]
        printMatrix(f"#0090239", layout)
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

        printMatrix("#09239i02", project_table)
        return project_table

    def mainWindow(self):
        """creates main window
        :return: main window
        """
        project_matrix = self.propperProjectMatrix()
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
            self.executeEvent(event=event, window=main_window)
            self.window_size = main_window.size #todo breaks down sometimes
            self.window_location = main_window.current_location()
            main_window.close()
            self.autoSave()


# todo complet documentation and code cleanup


if __name__ == '__main__':
    main_gui_task_atack = TaskAttack()

#todo kopieren löschen und verschieben von tasks

#todo scroll position beibehalten

#todo vllt sollte ich alle farbvergleiche auf stunden basis machen anstatt auf tage?!?

#todo when onely imputed "name" at saving it get saved as name not as name.tak












