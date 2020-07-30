__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"

import datetime
import textwrap
import time
from time import strftime

import PySimpleGUI as sg

import task, tools


def YesNoPopup(title:str, text:str, ok_button="Yes", cancel_button="No", size=(250, 70), keep_on_top=True,
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


class TaskFrameCreator:
    """
    Factory to create PySimpleGui Frames which represents either a Task or an empty space of the same size
    """

    @staticmethod
    def sSize():
        return 30


    @staticmethod
    def _basicTaskFrame(frame_name:str, name, priority, completed,
                        place_holder, option_button,
                        relief=sg.RELIEF_RAISED,
                        tooltip_text:str="", frame_color:str=None):
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
                         title=frame_name[:TaskFrameCreator.sSize()], relief=relief, size=(TaskFrameCreator.sSize() ,5),
                         tooltip=tooltip_text, background_color=frame_color)
        return frame

    @staticmethod
    def _toolTipText(task:task.Task):
        """
        :return: full plain textual representation of an task.Task() suitable as tooltip_text
        """
        tt = ""
        tt += f"   {task.HierarchyTreePositionString()}\n\n"
        tt += f"   {task.sName()}\n\n"
        tt += f"   Start: {task.sStart()}   Ende:{task.sEnde()}   PR: {task.sPriority():3d}   \n"
        tt += f"   Verbleibende Tage:.................................. {task.sRemainingDays()}   \n"
        tt += f"   Prozentualer Anteil am gesamt projekt:.. {task.sPercentage()}   \n"
        tt += f"   Anzahl Unteraufgaben:............................. {len(task.sSubTasks()) if task.sSubTasks() else '0'}   \n"
        tt += f"   Vollendet in Prozent:................................. {task.sCompleted():5.1f}   \n\n"
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
            return sg.Checkbox(text=" Completed", key=f"compl-#7#{str(task.sPosition())}", default=default,
                               enable_events=True, tooltip=tooltip_text, background_color=background_color)
        return sg.Text(f"Vollendet: {task.sCompleted():6.2f}", tooltip=tooltip_text, background_color=background_color)


    def _buttonMenuList(self):
        return ['Unused', ['Unteraufgabe', 'Isolieren', 'Bearbeiten', 'Löschen', 'Verschieben', 'Kopieren']]

    def _buttonMenu(self, task):
        return sg.ButtonMenu('Options', self._buttonMenuList(), key=f'-BMENU-#7#{task.sPosition()}')


    def taskFrame(self, task:task.Task):
        """
        :return: sg.Frame which represents the short Tree notation of an Task inclusive a full tooltip text
        """
        tooltip_text = self._toolTipText(task)
        background_color = task.taskDeadlineColor()

        name_sg_object = sg.Text(text=task.sName(), size=(self.sSize() - 5, 1), tooltip=tooltip_text, background_color=background_color)
        priority_sg_object = sg.Text(text=f"PR:.{task.sPriority():3d}", tooltip=tooltip_text, background_color=background_color)
        completed_sg_object = self._isCompletedElement(task, tooltip_text=tooltip_text, background_color=background_color)

        frame_name = task.HierarchyTreePositionString()

        aling_sg_object = sg.Text(text="", size=(self.sSize() - 15,1))
        option_button_sg_object = self._buttonMenu(task)

        frame = self._basicTaskFrame(frame_name=frame_name, name=name_sg_object, priority=priority_sg_object,
                                     completed=completed_sg_object,
                                     place_holder=aling_sg_object, option_button=option_button_sg_object,
                                     tooltip_text=tooltip_text, frame_color=background_color)
        return frame


    @staticmethod
    def emptyTaskFrame():
        """
        :return: empty sg.Frame in same size than a task frame
        """
        return sg.Frame(layout=[[sg.Text(text="", size=(TaskFrameCreator.sSize() -5, 5))]], title=" ",relief=sg.RELIEF_FLAT, size=(300, 50))


class TaskInputWindowCreator:
    """factory for task input windows on work on task input windows"""

    @staticmethod
    def _buttonLine():
        return [sg.Submit("Übernehmen"), sg.Cancel("Abbrechen")]

    @staticmethod
    def _updateWithDates(values, window):
        values.update({"start": datetime.datetime(*time.strptime(window['-START_BUTTON-'].get_text(), "%Y-%m-%d")[:6])})
        try:
            values.update({"ende": datetime.datetime(*time.strptime(window['-END_BUTTON-'].get_text(), "%Y-%m-%d")[:6])})
        except TypeError or ValueError:
            values.update({"ende":None})
        except ValueError:
            values.update({"ende":None})
        return values

    def inputValidation(self, window, masters_ende):
        while True:
            event, values = window.read()
            print(f"inputValidation; event: {event}, values: {values}")
            if event in {"Abbrechen", None}:
                break
            elif event == 'priority' and values['priority'] and values['priority'][-1] not in \
                        {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0"}:
                window['priority'].update(values['priority'][:-1])
            elif event == "Übernehmen":
                values = self._updateWithDates(values, window)
                print(f"#8972398u9  values: {values}, masters_ende: {masters_ende}")
                if masters_ende and values["ende"] and values["ende"] > masters_ende:
                    window['Ende-KORREKTUR-'].update("Nicht später als Master-Task-Ende")
                else:
                    break
            elif event == "Löschen":
                break
        try:
            values.update({'priority':int(values['priority'])})
        except ValueError:
            values.update({'priority':0})
        return event, values

    @staticmethod
    def _priorityLine(priority):
        """
        :param priority:
        :return:
        """
        return [sg.Text('Priorität: (1-99)', size=(15, 1)),
                sg.InputText(default_text=priority, key='priority', enable_events=True)]

    def calenderLine(self, calendar_date:datetime.datetime, s_or_e="Start", key='-START_BUTTON-', target='-START_BUTTON-'):
        """
        :param s_or_e: "Start" or "Ende"
        :param key: button key to fetch value
        :param target: button target key to update value
        :return: calendar line for either start or end
        """
        button_text, date_tuple = self.calendarButtonParameter(calendar_date=calendar_date, s_or_e=s_or_e)
        line = [sg.Text('Start:', size=(15, 1)),
                sg.CalendarButton(default_date_m_d_y=date_tuple, button_text=button_text,
                                  format="%Y-%m-%d", key=key, target=target),
                sg.Text(key=f'{s_or_e}-KORREKTUR-', text_color="#FF0000", size=(35, 1))]
        print(f"line... {line}")
        return line

    @staticmethod
    def _descriptionLine(description):
        """
        :param description: task description
        :return: label and description multiple line text input
        """
        return [sg.Text('Beschreibung:', size=(15, 1)),
                sg.Multiline(default_text=description, size=(45,20), key='description')]

    @staticmethod
    def _nameLine(kind:str, name:str):
        """
        :param kind: Aufgabe or Project
        :param name: task name
        :return: label and text input for nameline
        """
        return [sg.Text(f'{kind}name:', size=(15, 1)), sg.InputText(default_text=name, key='name')]

    @staticmethod
    def _calendarButtonText(calendar_date:datetime.datetime):
        """
        turns datetime.datetime in string "yyyy-mm-dd"
        :param calendar_date: datetime.datetime
        :return: string "yyyy-mm-dd"
        """
        calendar_text = strftime(f"%Y-%m-%d", calendar_date.timetuple())
        return calendar_text

    def calendarButtonParameter(self, calendar_date:datetime.datetime=None, s_or_e="Start"):
        """
        :param calendar_date: datetime.datetime
        :param s_or_e: string "Start" or "Ende"
        :return: string:calendar_text, tuple:calendar_date_tuple
        """
        if calendar_date:
            calendar_text = self._calendarButtonText(calendar_date)
        else:
            calendar_date = tools.nowDateTime()
            calendar_text = self._calendarButtonText(calendar_date) if s_or_e == "Start" else s_or_e
        calendar_date_tuple = (calendar_date.month, calendar_date.day, calendar_date.year)
        return calendar_text, calendar_date_tuple

    def inputWindow(self, kind:str, name:str='', description:str='',
                    start:datetime.datetime=None, ende:datetime.datetime=None,
                    priority='', masters_ende:datetime.datetime=None, keep_on_top=True,
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
        print(f"#90uojhajskd ende: {ende}")
        if not ende:
            ende = masters_ende

        layout = [
            self._nameLine(name=name, kind=kind),
            self._descriptionLine(description=description),
            self.calenderLine(calendar_date=start),
            self.calenderLine(calendar_date=ende, s_or_e="Ende", key='-END_BUTTON-', target='-END_BUTTON-'),
            self._priorityLine(priority=priority),
            self._buttonLine()
        ]
        window = sg.Window(kind, layout, keep_on_top=keep_on_top)
        event, values = self.inputValidation(window, masters_ende)
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
        print("blub")

        win_creator = TaskInputWindowCreator()
        event, values = win_creator.inputWindow(kind="Projekt", start=None)
        print(event, values)


