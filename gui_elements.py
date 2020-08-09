__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"

import datetime
import os
import sys
import textwrap
import time
from time import strftime

import PySimpleGUI as sg
from internationalisation import inter

import task, tools


def YesNoPopup(title:str, text:str, ok_button=inter.yes, cancel_button=inter.no, size=(250, 70), keep_on_top=True,
               *args, **kwargs):
    """
    popup window to do ok-chancel/yes-now and similar questions
    :param title: The title that will be displayed in the Titlebar and on the Taskbar
    :param text: The text that will be displayed in the popup
    :param ok_button: The text on the "ok button"
    :param cancel_button: the text on the "cancel button"
    :param size: size of the popup
    :param keep_on_top: If True, window will be created on top of all other windows on screen.
    :return: True or False corresponding to users button click
    """
    layout = [[sg.Text(text=text)],
              [sg.Button(button_text=ok_button), sg.Button(button_text=cancel_button)]]
    window = sg.Window(title=title, layout=layout, auto_size_buttons=True, keep_on_top=keep_on_top, size=size)
    event, values = window.read()
    window.close()
    if event == ok_button:
        return True
    return False

def _completeFilePathWithExtension(file_path, target_extension:str=".tak"):
    """
    checks file path for ".atk" extension and adds it if necessary
    :param file_path: "file_path_string"
    :return: "some "file_path_string.tak"
    """
    file_name, extension = os.path.splitext(file_path)
    print(f"check!!!::: {file_name} : {extension}")
    if not extension:
        file_path += target_extension
    return file_path


def newResultFilePopup(file_name:str, filetype:str, file_ext:str=".ods"):
    assert len(file_ext) == 4
    layout = [[sg.Text(inter.file_name, size=(15,1)),
               sg.Input(default_text=f"{file_name}.{file_ext}", size=(30,1), key='-FILE-NAME-'),
               sg.FileSaveAs(inter.save_at, file_types=((filetype, file_ext),), )],

              [sg.Text(inter.short_description, size=(15,1)),
               sg.Input(size=(30,1), enable_events=True, key='-SHORT_DESCRIPTIOM-'),
               sg.Ok()]]
    window = sg.Window(title=f"{filetype} erstellen", layout=layout)
    while True:
        event, values = window.read()
        if event is None:
            return None
        elif event == '-SHORT_DESCRIPTIOM-' and len(values['-SHORT_DESCRIPTIOM-']) > 30:
            window['-SHORT_DESCRIPTIOM-'].update(values['-SHORT_DESCRIPTIOM-'][:-1])
        elif event == "Ok":  #could be else but for fast later additions withoutt trouble i will be very precise
            file_name = values['-FILE-NAME-']
            file_name = _completeFilePathWithExtension(file_name, file_ext)
            short_description = values['-SHORT_DESCRIPTIOM-']
            print(f"file_name: {file_name}; short description: {short_description}")
            return file_name, short_description

newResultFilePopup("projedt_so", "Tabellenkalkulation", ".ods")

sys.exit(0)


class ResultFileCreator:

    def __init__(self):
        self._file_templates = {inter.writer:"/templates/writer_template.odt",
                                inter.spreadsheet:"/templates/spreadsheet_template.ods",
                                inter.presentation:"/templates/presentation_template.ods",
                                inter.drawing:"/templates/drawing_template.odg",
                                inter.database:"/templates/database_template.odb",
                                inter.gimp:"/templates/gimp_template.odb",
                                inter.inkscape:"/templates/inkscape_template.odb"}


    # def createResult(self, task, file_type):




class TaskFrameCreator:
    """
    Factory to create PySimpleGui Frames which represents either a Task or an empty space of the same size
    """

    def __init__(self, size=30):
        self.setBasichButtonMenuList()
        self.size = size

    def sSize(self):
        """
        :return: int:
        """
        return self.size

    def setSize(self, size:int):
        """
        :param size: sets width of a frame / x-axis size
        """
        self.size = size

    def _basicTaskFrame(self, frame_name:str, name, priority, completed, place_holder, option_button,
                        relief=sg.RELIEF_RAISED, tooltip_text:str="", frame_color:str=None):
        """task frame creation
        :param name: simplegu element name line
        :param priority: simplegui priority line
        :param completed: simplegui completed line
        :param edit: edit button
        :param add: add subtask button 
        :return: short task representation in a frame
        """
        frame = sg.Frame(layout=[[name],
                                 [priority, completed],
                                 [place_holder, option_button]
                                 ],
                         title=frame_name[-(self.sSize() -3):], relief=relief, size=(self.sSize() ,5),
                         tooltip=tooltip_text, background_color=frame_color)
        return frame

    @staticmethod
    def nAIt(wantet_value):
        return "N.A." if not wantet_value else wantet_value

    @staticmethod
    def _toolTipText(task:task.Task):
        """
        :return: full plain textual representation of an task.Task() suitable as tooltip_text
        """
        tt = ""
        tt += f"   {task.hierarchyTreePositionString()}\n\n"
        tt += f"   {task.sName()}\n\n"
        tt += f"   {inter.start}: {task.sStart()}   {inter.end}:v{TaskFrameCreator.nAIt(task.sEnde())}   {inter.priority}: {task.sPriority()}   \n"
        tt += f"   {inter.rem_days}:..................................... {TaskFrameCreator.nAIt(task.sRemainingDays())}   \n"
        tt += f"   {inter.project_part_percentage}:............... {task.sPercentage()}%   \n"
        tt += f"   {inter.sub_task_amount}:............................... {len(task.sSubTasks()) if task.sSubTasks() else '0'}   \n"
        tt += f"   {inter.percent_compled}:............................. {task.sCompleted():5.1f}%   \n\n"
        tt += "    \n   ".join(textwrap.wrap(task.sDescription(), width=90))

        return tt

    @staticmethod
    def _isCompletedElement(task:task.Task, tooltip_text, background_color:str):
        """
        builds up task completed line either an percentage, or an checkbox corresponding to kind of task
        :param background_color: hexstring like "#ff0000"
        :return: in frame layout usable completed line
        """
        default = True if task.sCompleted() else False
        if type(task.sCompleted()) == int:
            return sg.Checkbox(text=inter.completed, key=f"compl-#7#{str(task.sPosition())}", default=default,
                               enable_events=True, tooltip=tooltip_text, background_color=background_color)
        return sg.Text(f"{inter.completed}: {task.sCompleted():6.2f}", tooltip=tooltip_text, background_color=background_color)

    def _optionButtonMenuList(self):
        """
        :return: list of list, sg.ButtonMenu.layout for option button menu
        """
        return self._button_menu_list

    def setBasichButtonMenuList(self):
        """
        fetches basic option button menu list of list from internationalisation module
        """
        self._button_menu_list = inter.b_b_m_l

    def changeMenuListToIsolated(self):
        """
        fetches altered >tree view< option button menu list of list from internationalisation module
        """

        self._button_menu_list = inter.c_b_m_l

    def _buttonMenu(self, task):
        """
        :return: option menu button for every task frame
        """
        return sg.ButtonMenu(inter.options, self._optionButtonMenuList(), key=f'-BMENU-#7#{task.sPosition()}', border_width=2)


    def taskFrame(self, task:task.Task):
        """
        :return: sg.Frame which represents the short Tree notation of an Task inclusive a full tooltip text
        """
        tooltip_text = self._toolTipText(task)
        background_color = task.taskDeadlineColor()

        name_sg_object = sg.Text(text=task.sName(), size=(self.sSize() - 5, 1), tooltip=tooltip_text, background_color=background_color)
        priority_sg_object = sg.Text(text=f"{inter.short_pr}:.{task.sPriority():3d}", tooltip=tooltip_text, background_color=background_color)
        completed_sg_object = self._isCompletedElement(task, tooltip_text=tooltip_text, background_color=background_color)

        frame_name = task.hierarchyTreePositionString()

        aling_sg_object = sg.Text(text="", size=(self.sSize() - 15,1), background_color=background_color)
        option_button_sg_object = self._buttonMenu(task)

        frame = self._basicTaskFrame(frame_name=frame_name, name=name_sg_object, priority=priority_sg_object,
                                     completed=completed_sg_object,
                                     place_holder=aling_sg_object, option_button=option_button_sg_object,
                                     tooltip_text=tooltip_text, frame_color=background_color)
        return frame


    def emptyTaskFrame(self):
        """
        :return: empty sg.Frame in same size than a task frame
        """
        return sg.Frame(layout=[[sg.Text(text="", size=(self.sSize() -5, 5))]], title=" ",relief=sg.RELIEF_FLAT, size=(300, 50))


class TaskInputWindowCreator:
    """factory for task input windows on work on task input windows"""

    @staticmethod
    def _buttonLine():
        return [sg.Submit(inter.ok), sg.Cancel(inter.cancel)]

    @staticmethod
    def _updateWithDates(values, window):
        """updates window-values-dict with values fetched from date buttons"""
        values.update({"start": datetime.datetime(*time.strptime(window['-START_BUTTON-'].get_text(), "%Y-%m-%d")[:6])})
        try:
            values.update({"ende": datetime.datetime(*time.strptime(window['-END_BUTTON-'].get_text(), "%Y-%m-%d")[:6])})
        except TypeError or ValueError:
            values.update({"ende":None})
        except ValueError:
            values.update({"ende":None})
        return values

    def inputValidation(self, window, masters_ende, masters_priority):
        """validates imput for user abort,
        only entering int in priority and int() them already,
        subtask dont prolong master task"""
        while True:
            event, values = window.read()
            if event in {inter.cancel, None}:
                break
            elif event == 'priority' and masters_priority:
                if values['priority'] > masters_priority:
                    window['priority'].update(masters_priority)
                    window['priority-KORREKTUR-'].update(inter.not_less_important_than_master)
            elif event == inter.ok:
                values = self._updateWithDates(values, window)
                if masters_ende and values["ende"] and values["ende"] > masters_ende:
                    window['Ende-KORREKTUR-'].update(inter.not_later_than_master)
                else:
                    break
        return event, values

    @staticmethod
    def _priorityLine(priority, masters_priority):
        """
        :param priority:
        :return:
        """
        #todo beauty this two lines: AND sholud i let this like master is 6 initialvalue is 6
        # or better every initialvalue is 4 undless master is better?!?
        inital_value = priority if priority else masters_priority
        inital_value = inital_value if inital_value else 4

        return [sg.Text(f'{inter.priority}: (0-9)', size=(15, 1)),
                sg.Spin(values=[0,1,2,3,4,5,6,7,8,9], initial_value=inital_value,
                        size=(2,1), key='priority', enable_events=True),
                sg.Text(key='priority-KORREKTUR-', text_color="#FF0000", size=(35, 1))]
                # sg.InputText(default_text=priority, key='priority', enable_events=True)]

    def calenderLine(self, calendar_date:datetime.datetime, s_or_e=inter.start, key='-START_BUTTON-', target='-START_BUTTON-'):
        """
        :param s_or_e: "Start" or "Ende"
        :param key: button key to fetch value
        :param target: button target key to update value
        :return: calendar line for either start or end
        """
        button_text, date_tuple = self.calendarButtonParameter(calendar_date=calendar_date, s_or_e=s_or_e)
        line = [sg.Text(s_or_e, size=(15, 1)),
                sg.CalendarButton(default_date_m_d_y=date_tuple, button_text=button_text,
                                  format="%Y-%m-%d", key=key, target=target),
                sg.Text(key=f'{s_or_e}-KORREKTUR-', text_color="#FF0000", size=(35, 1))]
        return line

    @staticmethod
    def _descriptionLine(description):
        """
        :param description: task description
        :return: label and description multiple line text input
        """
        return [sg.Text(text=inter.description, size=(15, 1)),
                sg.Multiline(default_text=description, size=(45,20), key='description')]

    @staticmethod
    def _nameLine(kind:str, name:str):
        """
        :param kind: Aufgabe or Project
        :param name: task name
        :return: label and text input for nameline
        """
        return [sg.Text(text=f'{kind}name:', size=(15, 1)), sg.InputText(default_text=name, key='name')]

    @staticmethod
    def _calendarButtonText(calendar_date:datetime.datetime):
        """
        turns datetime.datetime in string "yyyy-mm-dd"
        :param calendar_date: datetime.datetime
        :return: string "yyyy-mm-dd"
        """
        calendar_text = strftime(f"%Y-%m-%d", calendar_date.timetuple())
        return calendar_text

    def calendarButtonParameter(self, calendar_date:datetime.datetime=None, s_or_e=inter.start):
        """
        :param calendar_date: datetime.datetime
        :param s_or_e: string "Start" or "Ende"
        :return: string:calendar_text, tuple:calendar_date_tuple
        """
        if calendar_date:
            calendar_text = self._calendarButtonText(calendar_date)
        else:
            calendar_date = tools.nowDateTime()
            calendar_text = self._calendarButtonText(calendar_date) if s_or_e == inter.start else s_or_e
        calendar_date_tuple = (calendar_date.month, calendar_date.day, calendar_date.year)
        return calendar_text, calendar_date_tuple

    def inputWindow(self, kind:str, name:str='', description:str='',
                    start:datetime.datetime=None, ende:datetime.datetime=None,
                    priority='', masters_priority=None, masters_ende:datetime.datetime=None, keep_on_top=True,
                    *args, **kwargs
                    ):
        """
        :param kind: Project or Aufgabe
        :param name: short header for task
        :param description: detailed description
        :param start: start datetime
        :param ende: ende datetime or None
        :param priority: priority for task (needed later on for sorting)
        :param masters_ende: master tasks end, since a subtask needs to be finished befor master task can finish as well
        :param existend: true if its a task to work on False if window is createt for a new task
        :param keep_on_top: keep this window on top (i think it should always be True
        :param args:
        :param kwargs:
        :return:
        """
        if not ende:
            ende = masters_ende


        layout = [
            self._nameLine(name=name, kind=kind),
            self._descriptionLine(description=description),
            self.calenderLine(calendar_date=start),
            self.calenderLine(calendar_date=ende, s_or_e=inter.end, key='-END_BUTTON-', target='-END_BUTTON-'),
            self._priorityLine(priority=priority, masters_priority=masters_priority),
            self._buttonLine()
        ]
        window = sg.Window(kind, layout, keep_on_top=keep_on_top)
        event, values = self.inputValidation(window, masters_ende, masters_priority)
        values = self._updateWithDates(values, window)
        window.close()
        return event, values


if __name__ == '__main__':
    start = datetime.datetime(*time.localtime()[:6])
    end = start + datetime.timedelta(days=8)
    task_here = task.Task(name="etwaesswoiihröiojwöoiefjmöoqweivjkmövvoiwjrvöoiwqerqs",
                          description="noch etwa, noch mehr, immer mehr mehr mehr emers",
                          start=start, end=end, priority=20)
    task_here.position = (2,3)
    window = sg.Window("test", layout=[[sg.Text("etwas text")]])
    while True:
        task_button_creator = TaskFrameCreator()
        button = task_button_creator.taskFrame(task_here)
        buttonb = task_button_creator.emptyTaskFrame()
        buttonc = task_button_creator.emptyTaskFrame()
        buttond = task_button_creator.emptyTaskFrame()
        buttone = task_button_creator.taskFrame(task_here)
        buttonf = task_button_creator.emptyTaskFrame()
        buttong = task_button_creator.emptyTaskFrame()
        buttonh = task_button_creator.emptyTaskFrame()
        buttoni = task_button_creator.taskFrame(task_here)
        event, values = window.read()
        print(event, values)
        # time.sleep(4)
        window.close()
        window = sg.Window("test", layout=[[button, buttonb, buttonc],
                                           [buttond, buttone, buttonf],
                                           [buttong, buttonh, buttoni]])

        win_creator = TaskInputWindowCreator()
        event, values = win_creator.inputWindow(kind="Projekt", start=None)
        print(event, values)

