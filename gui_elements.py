__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"

import datetime
import textwrap
import time
from time import strftime

import PySimpleGUI as sg

from taskatack import task, tools

def OkCancelPopup(title, text, ok_button="OK", cancel_button="Cancel", size=(250, 70), keep_on_top=True,
                  *args, **kwargs):
    layout = [[sg.Text(text=text)],
              [sg.Button(button_text=ok_button), sg.Button(button_text=cancel_button)]]

    window = sg.Window(title=title, layout=layout, auto_size_buttons=True, keep_on_top=keep_on_top, size=size)
    event, values = window.read()
    window.close()
    if event == ok_button:
        return True
    return False



class TaskFrameCreator:

    INCREMENT_DEBUG_ID = 0

    def _basicTaskFrame(self, frame_name, name, priority, completed, edit, add, relief=sg.RELIEF_RAISED, tooltip="",
                        frame_color=None):
        frame = sg.Frame(layout=[[name],
                                 [priority, completed],
                                 [edit, add]],
                         title=frame_name[:30], relief=relief, size=(30,5), tooltip=tooltip, background_color=frame_color)
        return frame


    def _toolTipText(self, task:task.Task):
        tt = ""
        tt += f"   {task.hierarchyTreePositionString()}\n\n"
        tt += f"   {task.sName()}\n\n"
        tt += f"   Start: {task.sStart()}   Ende:{task.sEnde()}   PR: {task.priority:3d}   \n"
        tt += f"   Verbleibende Tage:.................................. {task.sRemainingDays()}   \n"
        tt += f"   Prozentualer Anteil am gesamt projekt:.. {task.sPercentage()}   \n"
        tt += f"   Anzahl Unteraufgaben:............................. {len(task.sub_tasks) if task.sSubTasks() else '0'}   \n"
        tt += f"   Vollendet in Prozent:................................. {task.completed:5.1f}   \n\n"
        tt += "    \n   ".join(textwrap.wrap(task.sDescription(), width=90))
        return tt

    def _isCompletedElement(self, task, tooltip_text, background_color):
        default = True if task.completed else False
        if type(task.completed) == int:
            return sg.Checkbox(text="Completed", key=f"compl-{str(task.position)}", default=default,
                               enable_events=True, tooltip=tooltip_text, background_color=background_color)
        return sg.Text(f"Vollendet: {task.completed:6.2f}", tooltip=tooltip_text, background_color=background_color)

    def taskFrame(self, task:task.Task):


        tooltip_text = self._toolTipText(task)
        background_color = task.sTaskDeadlineColor()

        name_sg_object = sg.Text(task.sName(), size=(30, 1), tooltip=tooltip_text, background_color=background_color)
        priority_sg_object = sg.Text(f"PR:.{task.priority:3d}", tooltip=tooltip_text, background_color=background_color)
        completed_sg_object = self._isCompletedElement(task, tooltip_text=tooltip_text, background_color=background_color)

        frame_name = task.hierarchyTreePositionString()

        edit_button = sg.Button("Bearbeiten", key=f"bearb-{str(task.position)}", tooltip=tooltip_text)
        add_suptask_button = sg.Button("Unteraufgabe", key=f"subta-{str(task.position)}", tooltip=tooltip_text)

        frame = self._basicTaskFrame(frame_name=frame_name, name=name_sg_object, priority=priority_sg_object,
                                     completed=completed_sg_object, edit=edit_button, add=add_suptask_button,
                                     tooltip=tooltip_text, frame_color=background_color)
        return frame

    def emptyTaskFrame(self):
        name = sg.Text(" ", size=(30, 1))
        priority = sg.T()
        comleted_sg_object = sg.T()
        edit_button = sg.Button(" ", visible=False)
        add_subtask_button = sg.Button(" ", visible=False)
        frame = self._basicTaskFrame(frame_name="", name=name, priority=priority, completed=comleted_sg_object,
                                     edit=edit_button, add=add_subtask_button, relief=sg.RELIEF_FLAT)
        return frame







    # def taskFrame(self, task:task.Task=None):
    #     assert task
    #     dr = task.sDataRepresentation()
    #     description = sg.Text(dr["description"], size=(28, 1))
    #     tooltip_text = "\n".join(textwrap.wrap(dr["description"]))
    #     start, end = dr["start"], dr["ende"]
    #     print(f"#09ueu90 start: {start}, ende : {end}")
    #     start = sg.Text(f"{start.year}-{start.month}-{start.day}", size=(8, 1))
    #     end_tag = f"{end.year}-{end.month}-{end.day}" if end else end
    #     end = sg.Text(end_tag, size=(8, 1))
    #     #duration = sg.Text(f"noch {duration} Tage", size=(10, 1))
    #     priority = sg.Text(f"P {dr['priority'] if dr['priority'] else ''}", size=(10, 1))
    #     edit_button = sg.Button("Bearbeiten", key=f"bearb-{str(task.position)}")
    #     add_suptask_button = sg.Button("Unteraufgabe", key=f"subta-{str(task.position)}")
    #     # frame = sg.Frame(layout=[[description],
    #     #                          [start, end, priority],
    #     #                          #[#duration,
    #     #                          # priority],
    #     #                          [work_on, add_suptask]], title=name[:30], relief=sg.RELIEF_RAISED, size=(30,5))
    #     frame = self._basicTaskFrame(name=dr["name"], description=description, start=start, end=end,
    #                                  priority=priority, edit_button=edit_button, add_subtask_button=add_suptask_button,
    #                                  tooltip=tooltip_text)
    #     return frame

    # def emptyTaskFrame(self, master_name):
    #     description = sg.Text(" ", size=(30, 1))
    #     start = sg.T(justification=sg.TEXT_LOCATION_TOP_LEFT)
    #     end = sg.Text(f"{master_name}", justification=sg.TEXT_LOCATION_CENTER)
    #     # duration = sg.Text(f"noch {duration} Tage", size=(10, 1))
    #     priority = sg.T(justification=sg.TEXT_LOCATION_RIGHT)
    #     edit_button = sg.Button(" ", visible=False)
    #     add_subtask_button = sg.Button(" ", visible=False)
    #     frame = self._basicTaskFrame(name=" ", description=description, start=start, end=end,
    #                                  priority=priority, edit_button=edit_button, add_subtask_button=add_subtask_button,
    #                                  relief=sg.RELIEF_FLAT)
    #     return frame


class TaskInputWindowCreator:


    def nowDate(self):
        return datetime.datetime(*[int(x) for x in time.localtime(int(time.time()))[:6]])


    def _buttonLine(self, existend=False):
        if existend:
            return [sg.Submit("Übernehmen"), sg.Cancel("Abbrechen"), sg.Button("Löschen")]
        else:
            return [sg.Submit("Übernehmen"), sg.Cancel("Abbrechen")]



    def updateWithDates(self, values, window):
        values.update({"start": datetime.datetime(*time.strptime(window['-START_BUTTON-'].get_text(), "%Y-%m-%d")[:6])})
        try:
            values.update({"ende": datetime.datetime(*time.strptime(window['-END_BUTTON-'].get_text(), "%Y-%m-%d")[:6])})
        except:
            values.update({"ende":None})
        return values

    def inputValidation(self, window, masters_ende):
        while True:
            event, values = window.read()
            print(f"inputValidation; event: {event}, values: {values}")
            if event in {"Abbrechen", None #, "Übernehmen"
                         }:
                break

            elif event == 'priority' and values['priority'] and values['priority'][-1] not in {"1", "2", "3", "4",
                                                                                                     "5", "6", "7", "8",
                                                                                                     "9", "0"}:
                window['priority'].update(values['priority'][:-1])

            elif event == "Übernehmen":
                values = self.updateWithDates(values, window)
                print(f"#8972398u9  values: {values}, masters_ende: {masters_ende}")
                if masters_ende and values["ende"] and values["ende"] > masters_ende:
                    print(f"#lkasjfd 898 TROUBLE")
                    window['Ende-KORREKTUR-'].update("Nicht später als Master-Task-Ende")
                else:
                    break
            elif event == "Löschen":
                break

        try:
            values.update({'priority':int(values['priority'])})
        except:

            values.update({'priority':0})
        return event, values

    def _priorityLine(self, priority):
        return [sg.Text('Priorität: (1-99)', size=(15, 1)),
                sg.InputText(default_text=priority, key='priority', enable_events=True)]

    def _calenderLine(self, calendar_date, s_or_e="Start", key='-START_BUTTON-', target='-START_BUTTON-'):
        button_text, date_tuple = self.calendarButtonParameter(calendar_date=calendar_date, s_or_e=s_or_e)
        line = [sg.Text('Start:', size=(15, 1)),
                sg.CalendarButton(default_date_m_d_y=date_tuple, button_text=button_text,
                                  format="%Y-%m-%d", key=key, target=target),
                sg.Text(key=f'{s_or_e}-KORREKTUR-', text_color="#FF0000", size=(35, 1))]

        print(f"line... {line}")

        # f = [sg.Text('Ende:', size=(15, 1)), sg.CalendarButton(default_date_m_d_y=end_tuple, button_text=end_text, format="%Y-%m-%d", key='-END_BUTTON-', target='-END_BUTTON-'), sg.Text(key='-KORREKTUR-', text_color="#FF0000", size=(35, 1))],

        return line

    def _descriptionLine(self, description):
        return [sg.Text('Beschreibung:', size=(15, 1)), sg.Multiline(default_text=description, size=(45,20), key='description')]

    def _nameLine(self, kind, name):
        return [sg.Text(f'{kind}name:', size=(15, 1)), sg.InputText(default_text=name, key='name')]

    def calendarButtonText(self, calendar_date:datetime.datetime):
        """
        turns datetime.datetime in string "yyyy-mm-dd"
        :param calendar_date: datetime.datetime
        :return: string "yyyy-mm-dd"
        """
        print(f"calendar_date#198719u328 {calendar_date}")
        calendar_text = strftime(f"%Y-%m-%d", calendar_date.timetuple())
                # calendar_text = strftime(f"%a %d %m %Y", calendar_date.timetuple())
                # for en, de in self.day_mapping.items():
                #     calendar_text = calendar_text.replace(en, de)
        print(calendar_text)
        return calendar_text


    def calendarButtonParameter(self, calendar_date:datetime.datetime=None, s_or_e="Start"):
        """
        :param calendar_date: datetime.datetime
        :param s_or_e: string "Start" or "Ende"
        :return: string:calendar_text, tuple:calendar_date_tuple
        """
        if calendar_date:
            calendar_text = self.calendarButtonText(calendar_date)
        else:
            calendar_date = self.nowDate()
            calendar_text = self.calendarButtonText(calendar_date) if s_or_e == "Start" else s_or_e
        calendar_date_tuple = (calendar_date.month, calendar_date.day, calendar_date.year)
        return calendar_text, calendar_date_tuple

    def inputWindow(self, kind, name='', description='', start:datetime.datetime=None, ende:datetime.datetime=None,
                    priority='', masters_ende:datetime.datetime=None, existend=False,  keep_on_top=True,
                    *args, **kwargs):
        print(f"#90uojhajskd ende: {ende}")
        if not ende:
            ende = masters_ende

        self.layout = [
            #[sg.Text(f'{kind}name:', size=(15, 1)), sg.InputText(default_text=name, key='name')],
            self._nameLine(name=name, kind=kind),
            #[sg.Text('Beschreibung:', size=(15, 1)), sg.Multiline(default_text=description, size=(45,20), key='description')],
            self._descriptionLine(description=description),
            # [sg.Text('Start:', size=(15, 1)), sg.CalendarButton(default_date_m_d_y=start_tuple, button_text=start_text, format="%Y-%m-%d", key='-START_BUTTON-', target='-START_BUTTON-')],
            self._calenderLine(calendar_date=start),
            #[sg.Text('Ende:', size=(15, 1)), sg.CalendarButton(default_date_m_d_y=end_tuple, button_text=end_text, format="%Y-%m-%d", key='-END_BUTTON-', target='-END_BUTTON-'), sg.Text(key='-KORREKTUR-', text_color="#FF0000", size=(35, 1))],
            self._calenderLine(calendar_date=ende, s_or_e="Ende", key='-END_BUTTON-', target='-END_BUTTON-'),
            # [sg.Text('Priorität: (1-99)', size=(15, 1)), sg.InputText(default_text=priority, key='priority', enable_events=True)],
            self._priorityLine(priority=priority),
            # [sg.Submit("Übernehmen"), sg.Cancel("Abbrechen")]
            self._buttonLine(existend)
        ]
        window = sg.Window(kind, self.layout, keep_on_top=keep_on_top)
        event, values = self.inputValidation(window, masters_ende)
        values = self.updateWithDates(values, window)
        window.close()
        return event, values




if __name__ == '__main__':
        start = datetime.datetime(*time.localtime()[:6])
        end = start + datetime.timedelta(days=8)
        task_here = task.Task(name="etwaesswoiihröiojwöoiefjmöoqweivjkmövvoiwjrvöoiwqerqs", description="noch etwa, noch mehr, immer mehr mehr mehr emers", start=start, end=end, priority=20)
        task_here.position = (2,3)
        window = sg.Window("test", layout=[[sg.Text("etwas text")]])
        while True:
            task_button_creator = TaskFrameCreator()
            button = task_button_creator.taskFrame(task_here, master_gui=window)
            buttonb = task_button_creator.emptyTaskFrame()
            buttonc = task_button_creator.emptyTaskFrame()
            buttond = task_button_creator.emptyTaskFrame()
            buttone = task_button_creator.taskFrame(task_here, master_gui=window)
            buttonf = task_button_creator.emptyTaskFrame()
            buttong = task_button_creator.emptyTaskFrame()
            buttonh = task_button_creator.emptyTaskFrame()
            buttoni = task_button_creator.taskFrame(task_here, master_gui=window)
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


