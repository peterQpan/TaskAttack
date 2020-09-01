__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"

import datetime
import multiprocessing
import os
import shutil
import textwrap
import time
import warnings
from copy import deepcopy
from time import strftime
from typing import Any

import PySimpleGUI as sg
from colorama import Fore
from nose.util import file_like

import task
import tools
from internationalisation import inter


class RadioNew(sg.Frame):
    # todo ready to use but try to optimize by using
    """
    New because its Text isuneatable
    Radio Button Element - Used in a group of other Radio Elements to provide user with ability to select only
    1 choice in a list of choices.
    """

    def __init__(self, text, group_id, default=False, disabled=False, text_size=(None, None), rad_size=(None, None),
                 auto_size_text=None, background_color=None, text_color=None, font=None, key=None, rad_pad=(0, 0),
                 text_pad=(0, 0), pad=None,
                 tooltip=None, change_submits=False, enable_events=False, visible=True, metadata=None,
                 click_submits=False, relief=None, border_width=None, justification=None, right_click_menu=None,
                 element_justification="left"):
        """
        :param text: Text to display next to button
        :type text: (str)
        :param group_id: Groups together multiple Radio Buttons. Any type works
        :type group_id: (Any)
        :param default: Set to True for the one element of the group you want initially selected
        :type default: (bool)
        :param disabled: set disable state
        :type disabled: (bool)
        :param size: (width, height) width = characters-wide, height = rows-high
        :type size: (int, int)
        :param auto_size_text: if True will size the element to match the length of the text
        :type auto_size_text: (bool)
        :param background_color: color of background
        :type background_color: (str)
        :param text_color: color of the text
        :type text_color: (str)
        :param font: specifies the font family, size, etc
        :type font: Union[str, Tuple[str, int]]
        :param key: Used with window.FindElement and with return values to uniquely identify this element
        :type key: Union[str, int, tuple, object]
        :param k: Same as the Key. You can use either k or key. Which ever is set will be used.
        :type k: Union[str, int, tuple, object]
        :param pad: Amount of padding to put around element (left/right, top/bottom) or ((left, right), (top, bottom))
        :type pad: (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int)
        :param tooltip: text, that will appear when mouse hovers over the element
        :type tooltip: (str)
        :param change_submits: DO NOT USE. Only listed for backwards compat - Use enable_events instead
        :type change_submits: (bool)
        :param enable_events: Turns on the element specific events. Radio Button events happen when an item is selected
        :type enable_events: (bool)
        :param visible: set visibility state of the element
        :type visible: (bool)
        :param metadata: User metadata that can be set to ANYTHING
        :type metadata: (Any)
        :param click_submits: DO NOT USE. Only listed for backwards compat - Use enable_events instead
        :type click_submits: (bool)
        :param relief: relief style around the text. Values are same as progress meter relief values. Should be a constant that is defined at starting with "RELIEF_" - `RELIEF_RAISED, RELIEF_SUNKEN, RELIEF_FLAT, RELIEF_RIDGE, RELIEF_GROOVE, RELIEF_SOLID`
        :type relief: (str/enum)
        :param border_width: number of pixels for the border (if using a relief)
        :type border_width: (int)
        :param justification: how string should be aligned within space provided by size. Valid choices = `left`, `right`, `center`
        :type justification: (str)
        :param right_click_menu: A list of lists of Menu items to show when this element is right clicked. See user docs for exact format.
        :type right_click_menu: List[List[Union[List[str],str]]]
        :param title: text that is displayed as the Frame's "label" or title
        :type title: (str)
        :param layout: The layout to put inside the Frame
        :type layout: List[List[Elements]]
        :param title_color: color of the title text
        :type title_color: (str)
        :param title_location: location to place the text title.  Choices include: TITLE_LOCATION_TOP TITLE_LOCATION_BOTTOM TITLE_LOCATION_LEFT TITLE_LOCATION_RIGHT TITLE_LOCATION_TOP_LEFT TITLE_LOCATION_TOP_RIGHT TITLE_LOCATION_BOTTOM_LEFT TITLE_LOCATION_BOTTOM_RIGHT
        :type title_location: (enum)
        :param element_justification: All elements inside the Frame will have this justification 'left', 'right', 'center' are valid values
        :type element_justification: (str)
        """
        self.radio_key = f"{key}RADIO-"
        self.radio = sg.Radio(text="", group_id=group_id, default=default, disabled=disabled, size=rad_size,
                              auto_size_text=auto_size_text, background_color=background_color, text_color=text_color,
                              font=font, key=self.radio_key, pad=rad_pad, tooltip=tooltip,
                              change_submits=change_submits,
                              enable_events=enable_events, visible=visible, metadata=metadata)
        self.text_key = f"{key}TEXT-"
        self.text = sg.Text(text=text, size=text_size, auto_size_text=auto_size_text, click_submits=click_submits,
                            # enable_events=enable_events,
                            relief=relief, font=font, text_color=text_color,
                            background_color=background_color, border_width=border_width, justification=justification,
                            pad=text_pad, key=self.text_key, right_click_menu=right_click_menu, tooltip=tooltip,
                            visible=visible, metadata=metadata)
        self.layout = [[self.radio, self.text]]
        super().__init__(title="", layout=self.layout, relief=sg.RELIEF_FLAT, font=font, pad=pad,
                         border_width=border_width, key=f"{key}", tooltip=tooltip, right_click_menu=right_click_menu,
                         visible=visible, element_justification=element_justification, metadata=metadata)

    def Update(self, text=None, background_color=None, text_color=None, font=None, radio_value=None, disabled=None,
               visible=None):
        """
        Changes some of the settings for the Radio Button Element. Must call `Window.Read` or `Window.Finalize` prior
        :param text: new text to show
        :type value: (str)
        :param background_color: color of background
        :type background_color: (str)
        :param text_color: color of the text
        :type text_color: (str)
        :param font: specifies the font family, size, etc
        :type font: Union[str, Tuple[str, int]]
        :param visible: set visibility state of the element
        :type visible: (bool)
        :param radio_value: if True change to selected and set others in group to unselected
        :type radio_value: (bool)
        :param disabled: disable or enable state of the element
        :type disabled: (bool)
        :param visible: control visibility of element
        :type visible: (bool)
        """
        self.text.Update(value=text, background_color=background_color, text_color=text_color, font=font,
                         visible=visible)
        self.radio.Update(value=radio_value, disabled=disabled, visible=visible)
        super().Update(visible=visible)


class RadioRow(sg.Frame):
    """makes a horizontal radio button group"""

    GROUP_ID = 345678

    def __init__(self, all_values: tuple, active_value, disabled: bool, key: Any, group_id=None):
        """
        :param all_values: tuple of all values
        :param active_value: value which is supposed to be active
        :param disabled: true if elements are supposed to be disabled
        :return: sg.Frame() """
        self.values = all_values
        # self.value_index_mapping = {index: value for index, value in enumerate(all_values)}
        self.active = active_value
        self.disabled = disabled
        self.key = key

        self.group_id = self._take_id(group_id)

        layout, self.radios = self._horizontalLayout()

        super().__init__(title="", relief=sg.RELIEF_FLAT, layout=layout, pad=(0, 0), key=key)

    def _horizontalLayout(self):
        layout = []
        radios = []
        for value in self.values:
            print(f"#18u3209 ---> d_type: {value} -- : active_type -- {self.active}")
            if value == self.active:
                radio_button = RadioNew(text=value, group_id=self.group_id, default=True, disabled=self.disabled,
                                        key=f"{self.key}{value}")
            else:
                radio_button = RadioNew(text=value, group_id=self.group_id, default=False, disabled=self.disabled,
                                        key=f"{self.key}{value}")
            layout.append([radio_button])
            radios.append(radio_button)
        return layout

    def _take_id(self, group_id):
        if not group_id:
            group_id = self.__class__.GROUP_ID
            RadioRow.GROUP_ID += 1
        return group_id

    def getValue(self):
        for radio, value in zip(self.radios, self.values):
            if radio.get():
                return value


class MyGuiToolbox:

    @staticmethod
    def _okCancelLine(ok_button=inter.yes, cancel_button=inter.no,
                      key_ok="-OK-", key_cancel="-CANCEL-", left_padding=0):

        ok_button = sg.Button(button_text=ok_button, key=key_ok)
        cancel_button = sg.Button(button_text=cancel_button, key=key_cancel)
        if left_padding:
            padding = sg.Text(text=f"{' ' * left_padding}", key="-LEFT-PADDING-")
            return [padding, cancel_button, ok_button]
        return [cancel_button, ok_button]

    @staticmethod
    def YesNoPopup(title: str, text: str, ok_button=inter.yes, cancel_button=inter.no, size=(250, 70), keep_on_top=True,
                   key_ok="-OK-", key_cancel="-CANCEL-", *args, **kwargs):
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
        layout = [[sg.Text(text=text, auto_size_text=True)],
                  MyGuiToolbox._okCancelLine(ok_button=ok_button, cancel_button=cancel_button,
                                             key_ok=key_ok, key_cancel=key_cancel)]
        window = sg.Window(title=title, layout=layout, auto_size_buttons=True, keep_on_top=keep_on_top, size=size)
        event, values = window.read()

        window.close()
        if event == key_ok:
            return True
        return False

    # user_defined_keys
    # next above: ("-PFL", "-RFL", "-AsFL")
    # under-keys: ("-DE", "-IEX729X", "-FB")

    # user_defined_keys
    # next above: ("-SFL")
    # under-keys: ("-DE", "-IEX729X", "-FB")


class ResultFileCreator:

    def __init__(self):
        # self._external_threads = []
        self._file_templates = {inter.writer: ("/templates/writer_template.odt", ".odt"),
                                inter.spreadsheet: ("/templates/spreadsheet_template.ods", ".ods"),
                                inter.presentation: ("/templates/presentation_template.odp", ".odp"),
                                inter.drawing: ("/templates/drawing_template.odg", ".odg"),
                                inter.database: ("/templates/database_template.odb", ".odb"),
                                inter.gimp: ("/templates/gimp_template.xcf", ".xcf"),
                                inter.svg: ("/templates/inkscape_template.svg", ".svg")}

    @staticmethod
    def _newLayout(file_name, result_path, file_ext, kind_of_program):
        """creates new layout for file name / save as; short descripton pop up window"""
        print(f"initial folder: {os.path.join(result_path, os.path.split(file_name)[0])}")

        file_name_line = [sg.Text(inter.file_name, size=(15, 1)),
                          sg.Input(default_text=f"{file_name}{file_ext}", size=(30, 1), key='-FILE-NAME-'),
                          sg.FileSaveAs(inter.save_at, file_types=((kind_of_program, file_ext),),
                                        initial_folder=result_path, )]

        description_line = [sg.Text(inter.short_description, size=(15, 1)),
                            sg.Input(size=(30, 1), enable_events=True, key='-SHORT_DESCRIPTIOM-', focus=True),
                            sg.Ok()]
        return [file_name_line, description_line]

    @staticmethod
    def _correctInputEnforcement(window, values):
        """
        takes care that short description dont gets longer than 30 figures
        and that not the file_name <-> short desciption seperator gets used by the user
        """
        if len(values['-SHORT_DESCRIPTIOM-']) > 30:
            window['-SHORT_DESCRIPTIOM-'].update(values['-SHORT_DESCRIPTIOM-'][:-1])
        elif values['-SHORT_DESCRIPTIOM-'][-3:] == "<->":
            window['-SHORT_DESCRIPTIOM-'].update(values['-SHORT_DESCRIPTIOM-'][:-3])

    def _newResultFilePopup(self, suggested_file_name: str, result_path: str,
                            kind_of_program: str, file_ext: str = ".ods"):
        """
        gets file_name and short file description for new task result file
        :return: filename, short_description
        """
        assert len(file_ext) == 4
        layout = self._newLayout(file_name=suggested_file_name, file_ext=file_ext, kind_of_program=kind_of_program,
                                 result_path=result_path)
        window = sg.Window(title=inter.createResultFileTitle(kind_of_program=kind_of_program), layout=layout)
        while True:
            event, values = window.read()
            print(F"#099823 event: {event}; vlues: {values}")
            if event in (sg.WIN_CLOSED, None):
                return False, False
            elif event == '-SHORT_DESCRIPTIOM-':
                self._correctInputEnforcement(window=window, values=values)
            elif event == "Ok":  # could be else but for fast later additions withoutt trouble i will be very precise
                file_name, short_description = self._fetchResultFileParameters(
                    values=values, file_ext=file_ext, window=window)
                return file_name, short_description

    def _createAndOpenResultFile(self, kind_of_porogramm, file_path):
        template_file_path = self._file_templates[kind_of_porogramm][0]
        shutil.copy(tools.venvAbsPath(template_file_path), file_path)
        tools.openExternalFile(file_path=file_path  # , threads=self._external_threads
                               )

    @staticmethod
    def _fetchResultFileParameters(values, file_ext, window):
        """gets filename and short description from popup window and returns it"""
        file_name = values['-FILE-NAME-']
        file_path = tools.path.ensureFilePathExtension(file_name, file_ext)
        short_description = values['-SHORT_DESCRIPTIOM-']
        window.close()
        return file_path, short_description

    def newResultFile(self, task: task.Task, kind_of_porogramm, result_path):
        """
        creates new result file
        :param result_path: result path fetched from option.Option, no direct access here, so no import needed
        :param kind_of_porogram: inter.presentation, inter.spreadsheet, etc...
        """
        suggested_path, suggested_file_name = task.suggestetFileName(result_path)

        while True:
            user_file_path, description = self._newResultFilePopup(
                suggested_file_name=suggested_file_name, result_path=result_path,
                kind_of_program=kind_of_porogramm, file_ext=self._file_templates[kind_of_porogramm][1], )

            if user_file_path is False and description is False:
                break

            if user_file_path.startswith(os.sep): user_file_path = user_file_path[1:]
            user_path, user_file_name = os.path.split(user_file_path)

            if not user_path:
                tools.path.ensurePathExists(suggested_path)
                save_file_path = os.path.join(suggested_path, user_file_name)
            elif os.path.exists(user_path):
                save_file_path = user_file_path
            else:
                save_path = tools.path.chreateRootDestinguishedPaths(user_path=user_path, base_path=result_path)
                save_file_path = os.path.join(save_path, user_file_name)

            if os.path.isfile(save_file_path):
                if not MyGuiToolbox.YesNoPopup(title=inter.save_at, size=(None, None),
                                               text=f"{save_file_path}{inter.already_exists_override}"):
                    continue

            self._createAndOpenResultFile(kind_of_porogramm, save_file_path)
            task.addResultsFileAndDescription(save_file_path, description)
            break


# todo this time make a task frame creator wich inplements TaskFrame(Frame_class)
#  not necessary at this time

# todo think about maybe task frame creator is not necessary at all
# todo think about, which is better in performance??? because of update,
#  instead of renewal update is a big improvement,
#  and i dont have to keep track of all the sg-Elements... by frame inheritance

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

    def setSize(self, size: int):
        """
        :param size: sets width of a frame / x-axis size
        """
        self.size = size

    def _basicTaskFrame(self, frame_name: str, name_line: list, priority, completed, option_button_line: list,
                        relief=sg.RELIEF_RAISED, tooltip_text: str = "", frame_color: str = None):
        """task frame creation
        :param name: simplegu element name line
        :param priority: simplegui priority line
        :param completed: simplegui completed line
        :param edit: edit button
        :param add: add subtask button 
        :return: short task representation in a frame
        """
        frame = sg.Frame(layout=[name_line,
                                 [priority, completed],
                                 option_button_line],
                         title=frame_name[-(self.sSize() - 3):], relief=relief, size=(self.sSize(), 5),
                         tooltip=tooltip_text, background_color=frame_color)
        return frame

    @staticmethod
    def nAIt(wantet_value):
        return "N.A." if not wantet_value else wantet_value

    @staticmethod
    def _toolTipText(task: task.Task):
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
    def _isCompletedElement(task: task.Task, tooltip_text, background_color: str):
        """
        builds up task completed line either an percentage, or an checkbox corresponding to kind of task
        :param background_color: hexstring like "#ff0000"
        :return: in frame layout usable completed line
        """
        default = True if task.sCompleted() else False
        if type(task.sCompleted()) == int:
            return sg.Checkbox(text=inter.completed, key=f"compl-#7#{str(task.sPosition())}", default=default,
                               enable_events=True, tooltip=tooltip_text, background_color=background_color)
        return sg.Text(f"{inter.completed}: {task.sCompleted():6.2f}", tooltip=tooltip_text,
                       background_color=background_color)

    def sOptionButtonMenuList(self):
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

    def _buttonLinePlaceHolder(self, background_color, padding_size):
        # origiinal x_size: self.sSize() - 15
        return sg.Text(text="", size=(padding_size, 1), background_color=background_color)

    def _createButtonMenuWithResultFileEntrys(self, task):
        button_list = deepcopy(self.sOptionButtonMenuList())
        button_list[1][5] = []
        results = task.sResults()

        if results:
            for file_path, short_description in results:
                if short_description:
                    line = f"{short_description} <-> {file_path}"
                else:
                    line = f"{file_path}"
                button_list[1][5].append(line)
            return button_list

    def _buttonMenuLine(self, task, background_color):
        """
        :return: option menu button for every task frame
        """
        result_file_button_menu = self._createButtonMenuWithResultFileEntrys(task)

        # return sg.ButtonMenu(inter.options, original_button_list, key=f'-BMENU-#7#{task.sPosition()}',
        #                      border_width=2, )

        if result_file_button_menu:
            placeholer = self._buttonLinePlaceHolder(background_color=background_color, padding_size=self.sSize() - 20)
            image = sg.Image(filename="templates/file.png")
            option_button = sg.ButtonMenu(button_text=inter.options, menu_def=result_file_button_menu,
                                          key=f'-BMENU-#7#{task.sPosition()}')

            return [placeholer, image, option_button]

        else:
            placeholder = self._buttonLinePlaceHolder(background_color=background_color, padding_size=self.sSize() - 15)
            option_button = sg.ButtonMenu(button_text=inter.options, menu_def=self.sOptionButtonMenuList(),
                                          key=f'-BMENU-#7#{task.sPosition()}')
            return [placeholder, option_button]

    def taskFrame(self, task: task.Task):
        """
        :return: sg.Frame which represents the short Tree notation of an Task inclusive a full tooltip text
        """
        tooltip_text = self._toolTipText(task)
        background_color = task.taskDeadlineColor()

        name_line = self._nameLine(task=task, tooltip_text=tooltip_text, background_color=background_color)
        priority_sg_object = sg.Text(text=f"{inter.short_pr}:.{task.sPriority():3d}", tooltip=tooltip_text,
                                     background_color=background_color)
        completed_sg_object = self._isCompletedElement(task, tooltip_text=tooltip_text,
                                                       background_color=background_color)

        frame_name = task.hierarchyTreePositionString()

        button_menu_line = self._buttonMenuLine(task, background_color=background_color)

        frame = self._basicTaskFrame(frame_name=frame_name, name_line=name_line, priority=priority_sg_object,
                                     completed=completed_sg_object,
                                     option_button_line=button_menu_line,
                                     tooltip_text=tooltip_text, frame_color=background_color)
        return frame

    def _nameLine(self, task, tooltip_text, background_color):
        name_line = [sg.Text(text=task.sName(), size=(self.sSize() - 5, 1), tooltip=tooltip_text,
                             background_color=background_color)]
        return name_line

    def emptyTaskFrame(self):
        """
            :return: empty sg.Frame in same size than a task frame
            """
        return sg.Frame(layout=[[sg.Text(text="", size=(self.sSize() - 5, 5))]], title=" ", relief=sg.RELIEF_FLAT,
                        size=(300, 50))


"""in order to tackle this shortcut key thing i need my own task frames, i didnt do it i the first place because 
pysimplegui documentation said if you starting with making your own windows class you probably got it all wrong, so 
i tried to stick to the functional approach of py simple gui, but i think it would become very ugly at this point. 
shall i do a class wich can be utalized from task frame creator, so i dont have to change any code, 
or should i do it from scratch?!?, i think i first do the task frame creator approach, without any major code changes"""


class TaskFrame(sg.Frame):

    def __init__(self, task: task.Task = None, size=30):

        self.size = size
        self.setBasichButtonMenuList()

        if task:
            self.task = task
            print(f"#9923u0923 key for frame: {f'-MY-TASK-FRAME-{str(self.task.sPosition())}'}")
            self.key = F"-MY-TASK-FRAME-{str(self.task.sPosition())}"
            self.taskFrame() #superMethod
        else:
            self.emptyTaskFrame()#superMethod

    def sSize(self):
        """
        :return: int
        :type int
        """
        return self.size

    # def setSize(self, size: int):
    #     """
    #     :param size: sets width of a frame / x-axis size
    #     """
    #     self.size = size

    @staticmethod
    def nAIt(wantet_value):
        return "N.A." if not wantet_value else wantet_value

    # todo think about as now taskFrames are are real classes, should this methods remain static?!?
    @staticmethod
    def _toolTipText(task: task.Task):
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
    def _isCompletedElement(task: task.Task, tooltip_text, background_color: str):
        """
        builds up task completed line either an percentage, or an checkbox corresponding to kind of task
        :param background_color: hexstring like "#ff0000"
        :return: in frame layout usable completed line
        """
        default = True if task.sCompleted() else False
        if type(task.sCompleted()) == int:
            print(f"#0923ßn checkboxkey: {f'compl-#7#{str(task.sPosition())}'}")
            return sg.Checkbox(text=inter.completed, key=f"compl-#7#{str(task.sPosition())}", default=default,
                               enable_events=True, tooltip=tooltip_text, background_color=background_color)
        return sg.Text(f"{inter.completed}: {task.sCompleted():6.2f}", tooltip=tooltip_text,
                       background_color=background_color, key=f"COMPL-TEXT{task.sPosition()}")

    def sOptionButtonMenuList(self):
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

    def _buttonLinePlaceHolder(self, background_color, padding_size):
        # origiinal x_size: self.sSize() - 15
        return sg.Text(text="", size=(padding_size, 1), background_color=background_color)

    def _createButtonMenuWithResultFileEntrys(self):
        button_list = deepcopy(self.sOptionButtonMenuList())
        button_list[1][5] = []
        results = self.task.sResults()

        if results:
            for file_path, short_description in results:
                if short_description:
                    line = f"{short_description} <-> {file_path}"
                else:
                    line = f"{file_path}"
                button_list[1][5].append(line)
            return button_list

    def _buttonMenuLine(self, background_color):
        """
        :return: option menu button for every task frame
        """
        result_file_button_menu_list = self._createButtonMenuWithResultFileEntrys()

        if result_file_button_menu_list:
            placeholer = self._buttonLinePlaceHolder(background_color=background_color, padding_size=self.sSize() - 20)
            image = sg.Image(filename="templates/file.png")
            option_button = sg.ButtonMenu(button_text=inter.options, menu_def=result_file_button_menu_list,
                                          key=f'-BMENU-#7#{self.task.sPosition()}')

            return [placeholer, image, option_button]

        else:
            placeholder = self._buttonLinePlaceHolder(background_color=background_color, padding_size=self.sSize() - 15)
            option_button = sg.ButtonMenu(button_text=inter.options, menu_def=self.sOptionButtonMenuList(),
                                          key=f'-BMENU-#7#{self.task.sPosition()}')
            return [placeholder, option_button]

    def _nameLine(self, tooltip_text, background_color):
        """Key: f"{self.key}NAME-L-"
        :param tooltip_text:
        :param background_color:
        :return:
        """
        name_line = [sg.Text(text=self.task.sName(), size=(self.sSize() - 5, 1), tooltip=tooltip_text,
                             background_color=background_color, key=f"{self.key}NAME-L-")]
        return name_line

    def _basicTaskFrame(self, frame_name: str, name_line: list, priority_completed_line, option_button_line: list,
                        relief=sg.RELIEF_RAISED, tooltip_text: str = "", frame_color: str = None):
        """task frame creation
        :param name: simplegu element name line
        :param priority: simplegui priority line
        :param completed: simplegui completed line
        :param edit: edit button
        :param add: add subtask button
        :return: short task representation in a frame
        """
        super(TaskFrame, self).__init__(layout=[name_line,
                                                priority_completed_line,
                                                option_button_line],
                                        title=frame_name[-(self.sSize() - 3):], relief=relief, size=(self.sSize(), 5),
                                        tooltip=tooltip_text, background_color=frame_color, key=self.key)

    def taskFrame(self):
        """
        :return: sg.Frame which represents the short Tree notation of an Task inclusive a full tooltip text
        """
        tooltip_text = self._toolTipText(self.task)
        background_color = self.task.taskDeadlineColor()

        name_line = self._nameLine(tooltip_text=tooltip_text, background_color=background_color)

        prio_completed_line = self._priorityCompletedLine(tooltip_text=tooltip_text, background_color=background_color)

        frame_name = self.task.hierarchyTreePositionString()

        button_menu_line = self._buttonMenuLine(background_color=background_color)

        self._basicTaskFrame(frame_name=frame_name, name_line=name_line, priority_completed_line=prio_completed_line,
                             option_button_line=button_menu_line, tooltip_text=tooltip_text,
                             frame_color=background_color)

    def emptyTaskFrame(self):
        """
        :return: empty sg.Frame in same size than a task frame
        """
        super(TaskFrame, self).__init__(layout=[[sg.Text(text="", size=(self.sSize() - 5, 5))]], title=" ",
                                        relief=sg.RELIEF_FLAT,
                                        size=(300, self.size + 20))

    def _completeUpdate(self, window, key, value, background_color, tooltip_text):
        """makes a complete update of an sg.element text, bg_color AND tooltip_text"""
        window[key].Update(value=value, background_color=background_color)
        window[key].SetTooltip(tooltip_text=tooltip_text)

    def _updateFixedElements(self, window, background_color, tooltip_text):
        """Updates all elements in Task frame which never changes like sg.TExt <-> sg.Checkbox"""
        self._completeUpdate(
            window=window, key=f"{self.key}NAME-L-", value=self.task.sName(), background_color=background_color,
            tooltip_text=tooltip_text)
        self._completeUpdate(
            window=window, key=f"{self.key}PRIORITY-", value=f"{inter.short_pr}:.{self.task.sPriority():3d}",
            background_color=background_color, tooltip_text=tooltip_text)

    def _updateChangingElements(self, window, background_color, tooltip_text):
        """Updates all elements in Task frame which changes like sg.TExt <-> sg.Checkbox"""

        element = window.Element(key=f"compl-#7#{str(self.task.sPosition())}", silent_on_error=True)
        if element:
            self._completeUpdate(
                window=window, key=f"compl-#7#{str(self.task.sPosition())}", value=None,
                background_color=background_color, tooltip_text=tooltip_text)
        else:
            self._completeUpdate(
                window=window, key=f"COMPL-TEXT{self.task.sPosition()}", value=None,
                background_color=background_color, tooltip_text=tooltip_text)

    def Update(self, window, value=None, visible=None):
        """overriding of method wich enables the direct window[key] access
        and passes it along to the containing elements"""
        tooltip_text = self._toolTipText(self.task)
        background_color = self.task.taskDeadlineColor()
        frame_name = self.task.hierarchyTreePositionString()

        print(f"#09288309u parentWindow: {self.ParentWindow}")
        self._updateFixedElements(window=window, background_color=background_color, tooltip_text=tooltip_text)
        self._updateChangingElements(window=window, background_color=background_color, tooltip_text= tooltip_text)

        super(TaskFrame, self).Update(value=frame_name)
        self.SetTooltip(tooltip_text=tooltip_text)

    def _priorityCompletedLine(self, tooltip_text, background_color, ):
        priority_sg_object = sg.Text(text=f"{inter.short_pr}:.{self.task.sPriority():3d}", tooltip=tooltip_text,
                                     background_color=background_color, key=f"{self.key}PRIORITY-")
        completed_sg_object = self._isCompletedElement(self.task, tooltip_text=tooltip_text,
                                                       background_color=background_color)
        return [priority_sg_object, completed_sg_object]


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
            values.update(
                {"ende": datetime.datetime(*time.strptime(window['-END_BUTTON-'].get_text(), "%Y-%m-%d")[:6])})
        except TypeError or ValueError:
            values.update({"ende": None})
        except ValueError:
            values.update({"ende": None})
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
                    window['priority-KORREKTUR-'].update(inter.really_less_important_than_master)
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
        inital_value = priority if priority else masters_priority
        inital_value = inital_value if inital_value else 5

        return [sg.Text(f'{inter.priority}: {inter.low} (0-9) {inter.high}', size=(15, 1)),
                sg.Spin(values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], initial_value=inital_value,
                        size=(2, 1), key='priority', enable_events=True),
                sg.Text(key='priority-KORREKTUR-', text_color="#FF0000", size=(35, 1))]
        # sg.InputText(default_text=priority, key='priority', enable_events=True)]

    def _calenderLine(self, calendar_date: datetime.datetime, s_or_e=inter.start, key='-START_BUTTON-',
                      target='-START_BUTTON-'):
        """
        :param s_or_e: "Start" or "Ende"
        :param key: button key to fetch value
        :param target: button target key to update value
        :return: calendar line for either start or end
        """
        button_text, date_tuple = self._calendarButtonParameter(calendar_date=calendar_date, s_or_e=s_or_e)
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
                sg.Multiline(default_text=description, size=(45, 20), key='description')]

    @staticmethod
    def _nameLine(kind: str, name: str):
        """
        :param kind: Aufgabe or Project
        :param name: task name
        :return: label and text input for nameline
        """
        return [sg.Text(text=f'{kind}name:', size=(15, 1)), sg.InputText(default_text=name, key='name')]

    @staticmethod
    def _calendarButtonText(calendar_date: datetime.datetime):
        """
        turns datetime.datetime in string "yyyy-mm-dd"
        :param calendar_date: datetime.datetime
        :return: string "yyyy-mm-dd"
        """
        calendar_text = strftime(f"%Y-%m-%d", calendar_date.timetuple())
        return calendar_text

    def _calendarButtonParameter(self, calendar_date: datetime.datetime = None, s_or_e=inter.start):
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

    def inputWindow(self, kind: str, name: str = '', description: str = '',
                    start: datetime.datetime = None, ende: datetime.datetime = None,
                    priority='', masters_priority=None, masters_ende: datetime.datetime = None, keep_on_top=True,
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
            self._calenderLine(calendar_date=start),
            self._calenderLine(calendar_date=ende, s_or_e=inter.end, key='-END_BUTTON-', target='-END_BUTTON-'),
            self._priorityLine(priority=priority, masters_priority=masters_priority),
            self._buttonLine()
        ]
        window = sg.Window(kind, layout, keep_on_top=keep_on_top)
        event, values = self.inputValidation(window, masters_ende, masters_priority)
        print(F"#0823823 event: {event}; vlues: {values}")
        values = self._updateWithDates(values, window)
        window.close()
        return event, values


class OptionWindow:

    def _setDisabledStatusToUserDirectoryFrame(self, window: sg.Window, disabled: bool):
        """option-window
        sets user directory choice frame text in red or green and buttons enabled and disabled
        :param window: option_window
        :param disabled: bool is true if user chooses to make distinct saving directory
        frame key:
        next above: ("-PFL", "-RFL", "-AsFL")
        under-keys: ("-DE":color, "-IEX729X":disabled, "-FB":disabled)

        """
        text_color = "#ff0000" if disabled else "#00ff00"
        for first_part in ("-PFL", "-RFL", "-AsFL"):
            window[f"{first_part}-DE"].Update(text_color=text_color)
            window[f"{first_part}-IEX729X"].Update(disabled=disabled)
            window[f"{first_part}-FB"].Update(disabled=disabled)

    def _setDisabledStatusToStandardDirectoryFrame(self, window: sg.Window, disabled: bool):
        """option-window
        sets standard directory choice frame text in red or green and buttons enabled and disabled
        :param window: option_window
        :param disabled: bool is true if user chooses to make standard saving directory
        next above: ("-SFL")
        under-keys: ("-DE":color, "-IEX729X":disabled, "-FB":disabled)
        """
        text_color = "#ff0000" if disabled else "#00ff00"
        window["-SFL-DE"].Update(text_color=text_color)
        window["-SFL-IEX729X"].Update(disabled=disabled)
        window["-SFL-FB"].Update(disabled=disabled)

    def _horizontalRadioChoiceFrame(self, all_types: tuple, active_type, disabled, key: str, group_id="dura_radio"):
        """option-window
        makes a horizontal radio button group
        :param all_types: tuple of all values
        :param active_type: value which is supposed to be active
        :param disabled: needed if elements are supposed to be enablede
        :return: sg.Frame()
        """
        warnings.warn("use RadioRow instead", DeprecationWarning)
        layout = []
        for index, d_type in enumerate(all_types):
            print(f"#18u3209 ---> d_type: {d_type} -- : active_type -- {active_type}")
            if d_type == active_type:
                radio_button = RadioNew(text=d_type, group_id=group_id, default=True, disabled=disabled,
                                        key=f"{key}{index}")
            else:
                radio_button = RadioNew(text=d_type, group_id=group_id, default=False, disabled=disabled,
                                        key=f"{key}{index}")
            layout.append([radio_button])
        frame = sg.Frame(title="", relief=sg.RELIEF_FLAT, layout=layout, pad=(0, 0))
        return frame

    def _setDurationRadiosWithNewLanguage(self, all_types: tuple, key: str, window):
        """
        option-window
        sets new language for duration radio buttons
        :param all_types: inter tuple of duration types (days, pieces)
        :param key: key used for _horizontalRadioChoiceFrame()
        """
        for index, d_type in enumerate(all_types):
            print(f"#02934u key index: {key}{index}, type: {window[f'{key}{index}']}")
            window[f"{key}{index}"].Update(text=d_type)

    def autoSaveSettingInputFrame(self, duration_type: str, duration: int, disabled: bool,
                                  enable_radio_button: sg.Radio):
        """option-window
        frame for auto save file handeling setting"
        :param duration_type: inter.days or inter.pieces indicates actual settings
        :param duration: actual duration setting
        :param disabled: True if no auto save handeln
        :param enable_radio_button: sg.Radio()
        :return: sg.Frame
        """
        duration_type_radio_frame = self._horizontalRadioChoiceFrame(all_types=inter.duration_types,
                                                                     active_type=duration_type, disabled=disabled,
                                                                     key="-AUS-1-")
        duration_entry = sg.Input(default_text=duration, disabled=disabled, enable_events=True, size=(4, 1),
                                  key="-AUS-2-")
        layout = [[enable_radio_button, duration_entry, duration_type_radio_frame]]
        frame = sg.Frame(title="", layout=layout, relief=sg.RELIEF_FLAT, pad=(0, 0))
        return frame

    @staticmethod
    def _setImputAutoSaveFrame(window, disabled):
        window["-AUS-1-0"].Update(disabled=disabled)
        window["-AUS-1-1"].Update(disabled=disabled)
        window["-AUS-2-"].Update(disabled=disabled)

    def _autoSaveFileHandlingRulesFrame(self, duration_type: str, duration: int, autosave_handeling: bool):
        """option-window
        complete frame for auto save file handling
        :param duration_type: inter.days or inter.pieces indicates actual settings
        :param duration: actual duration setting
        :param autosave_handeling: actual setting, True if auto save files are handeled
        :return: layout line: [sg.frame]
        """
        no_auto_save_handling_radio_b = RadioNew(
            text=inter.no_autosave_deletion, group_id="autosave_deletion", default=(not autosave_handeling),
            enable_events=True, text_size=(30, 1), key="-AUTO-S-1-")
        auto_save_handeling_radio_b = RadioNew(
            text=inter.autosave_deletion, group_id="autosave_deletion", default=autosave_handeling,
            enable_events=True, text_size=(30, 1), key="-AUTO-S-2-")
        auto_save_setting_frame = self.autoSaveSettingInputFrame(
            duration_type=duration_type, duration=duration, disabled=(not autosave_handeling),
            enable_radio_button=auto_save_handeling_radio_b)
        layout = [[no_auto_save_handling_radio_b], [auto_save_setting_frame]]

        frame = sg.Frame(title="", layout=layout)
        return [frame]

    def _folderLine(self, name: str, directory: file_like, disabled: bool, key):
        """option-window
        creates a folder input line [sg.Text, sg.Input, sg.FolderBrowse]
        :param name: line description
        :param directory: actual directory
        :param disabled: disables complete line
        :param key: master_key for this line, becomes sub keys: -DE, -IEX729X, -FB
        :return: layout line: [sg.Text, sg.Input, sg.FolderBrowse]
        """
        text_color = "#ff0000" if disabled else "#00ff00"
        directory = directory if directory else ""
        description_elemetn = sg.Text(text=name, size=(15, 1), text_color=text_color, key=f"{key}-DE")
        input_element = sg.Input(default_text=directory, size=[25, 1], disabled=disabled, key=f"{key}-IEX729X",
                                 enable_events=True)
        folder_button = sg.FolderBrowse(button_text=inter.browse, disabled=disabled, key=f"{key}-FB")

        return [description_elemetn, input_element, folder_button]

    def _userDefinedFolderStructureFrame(self, directorys: dict, disabled):
        """option-window
        Frame for user commanded save directory structure
        :param directorys: directorys for (*.tak, results, autosave.tak
        :param disabled: disabled if standard folder structure is used
        :return: sg.Frame
        """
        user_decission_element_ind = RadioNew(
            text=inter.own_folder_setup, group_id="folder_setup", enable_events=True,
            default=(not disabled), key="-RADIO_2-")
        project_folder_line = self._folderLine(
            name=inter.project_folder, disabled=disabled, directory=directorys["main_folder"], key="-PFL")
        result_folder_line = self._folderLine(
            name=inter.results_folder, disabled=disabled, directory=directorys["result_folder"], key="-RFL")
        autosave_folder_line = self._folderLine(
            name=inter.auto_save_folder, disabled=disabled, directory=directorys["autosave_folder"], key="-AsFL")
        layout = [[user_decission_element_ind], project_folder_line, result_folder_line, autosave_folder_line]

        return sg.Frame(title="", layout=layout, relief=sg.RELIEF_FLAT)

    def _standardFolderStructureFrame(self, directorys, disabled):
        """option-window
        Frame for user commanded save directory structure
        :param directorys: directorys for (*.tak, results, autosave.tak
        :param disabled: disabled if standard folder structure is used
        :return: sg.Frame
        """
        user_decission_element_std = RadioNew(
            text=inter.standard_folder_setup, group_id="folder_setup", enable_events=True,
            default=(not disabled), key="-RADIO_1-")
        project_folder_line = self._folderLine(
            name=inter.results, disabled=disabled, directory=directorys["standard_main_folder"], key="-SFL")
        placeholder_s = [[sg.Text(text="", pad=(5, 7))] for _ in range(2)]

        layout = [[user_decission_element_std], project_folder_line, *placeholder_s]

        return sg.Frame(title="", layout=layout, relief=sg.RELIEF_FLAT)

    def _FolderStuchturLayoutLine(self, directorys: dict, wich_disabled: str):
        """optioln-window
        complete save folder line, standard AND user decided
        :param directorys: actual folders
        :param wich_enabled: "ind" or "std"
        :return: complete save folder line: [sg.Frame]
        """
        print(f"#03923i wich disabled: {wich_disabled}")
        if wich_disabled == "ind":
            layout = [[self._standardFolderStructureFrame(directorys=directorys, disabled=False),
                       self._userDefinedFolderStructureFrame(directorys=directorys, disabled=True)]]
        else:
            layout = [[self._standardFolderStructureFrame(directorys=directorys, disabled=True),
                       self._userDefinedFolderStructureFrame(directorys=directorys, disabled=False)]]
        folder_structur_line = sg.Frame(title="", layout=layout)
        return [folder_structur_line]

    def _languageTextFrame(self):
        """option-window
        creates an frame three elements high to match listbox in height and align accordingly
        :return: sg.Frame
        """
        layout = [[sg.Text(text=f"{inter.language}     ", key="language-t-f", size=(10, 1))], [sg.Text()], [sg.Text()]]
        print(f"layout litzr: {layout}")

        frame = sg.Frame(title="", layout=layout, relief=sg.RELIEF_FLAT)
        return frame

    def _languageSettingsLine(self, actual_language: str):
        """option-window
        complete language frame with text and listbox in a line
        :param actual_language:
        :return: complete language line: [sg.Frame, sg.Listbox]
        """
        language_text_frame = self._languageTextFrame()
        language_selection_List_box = sg.Listbox(values=inter.sLanguages(), default_values=[actual_language],
                                                 size=(10, 4), select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                                                 enable_events=True, key="-LANGUAGE-")
        return [language_text_frame, language_selection_List_box]

    def _completeOptionWindowLayout(self, directorys: dict, disabled_folder_usage: str, language: str,
                                    autosave_handling: bool, autosave_amount_type: str, autosave_amount: int,
                                    *args, **kwargs):
        """option-window
        gathers all lines together ond creates final layout line
        :param directorys: achtual_directorys
        :param disabled_folder_usage: "ind" or "std" --> individual - standard
        :param language:
        :param autosave_handling: if auto save handling
        :param autosave_amount_type: actualy set duration type inter.days or inter.pieces
        :param autosave_amount: actualy set duration amount
        :return: final layout line [self.line, self.line, self.line]
        """
        return [self._languageSettingsLine(language),
                self._FolderStuchturLayoutLine(directorys=directorys, wich_disabled=disabled_folder_usage),
                self._autoSaveFileHandlingRulesFrame(
                    duration_type=autosave_amount_type, duration=autosave_amount, autosave_handeling=autosave_handling),
                MyGuiToolbox()._okCancelLine(ok_button=inter.ok, cancel_button=inter.cancel,
                                             left_padding=inter.left_pading_amounts["deutsch"])]

    def setLanguageAnew(self, values, event, window):
        """
        sets language directly anew in option window, all other windows will it do automatically by window reload
        """

        choosen_language = values[event][0]
        inter.setLanguage(choosen_language)

        self._setDurationRadiosWithNewLanguage(all_types=inter.duration_types, key="-AUS-1-", window=window)
        self._setDirectoryFramesWithNewLanguage(window=window)

        window_keys = [f"-SFL-DE", "language-t-f", "-RADIO_1-", "-RADIO_2-", "-AUTO-S-1-", "-AUTO-S-2-", "-CANCEL-",
                       "-OK-", "-LEFT-PADDING-"]
        propertys = [inter.project_folder, inter.language, inter.standard_folder_setup, inter.own_folder_setup,
                     inter.no_autosave_deletion, inter.autosave_deletion, inter.cancel, inter.ok,
                     ' ' * inter.left_pading_amounts[choosen_language]]

        for key, property in zip(window_keys, propertys):
            try:
                window[key].Update(text=property)
            except TypeError as e:
                window[key].Update(value=property)

    def _setDirectoryFramesWithNewLanguage(self, window):
        """
        sets language in directory frames
        """
        for key, text in {"-PFL": inter.project_folder, "-RFL": inter.results, "-AsFL": inter.auto_save_folder}.items():
            print(f"key 0932u5: {key}-DE")
            window[f"{key}-DE"].Update(value=text)

    def inputValidation(self, event, values, window, actual_language):
        if event is None or event in (sg.WIN_CLOSED, "Abbrechen", "-CANCEL-"):
            inter.setLanguage(actual_language)
            return True
        if "-IEX729X" in event:
            if r"//" in values[event]:
                window[event].Update(values[event].replace("//", "/"))
        if event == "-RADIO_1-RADIO-":  # todo RadioNew clutters the code with his destinct own keys, needs a better inheritance for clearer code
            self._setDisabledStatusToStandardDirectoryFrame(window=window, disabled=False)
            self._setDisabledStatusToUserDirectoryFrame(window=window, disabled=True)

        elif event == "-RADIO_2-RADIO-":
            self._setDisabledStatusToStandardDirectoryFrame(window=window, disabled=True)
            self._setDisabledStatusToUserDirectoryFrame(window=window, disabled=False)

        elif event == "-AUTO-S-1-RADIO-":
            self._setImputAutoSaveFrame(window=window, disabled=True)
        elif event == "-AUTO-S-2-RADIO-":
            self._setImputAutoSaveFrame(window=window, disabled=False)
        elif event == "-LANGUAGE-":
            self.setLanguageAnew(values=values, event=event, window=window)
        elif event == "-OK-":
            self.outcome = event, values
            return True

    def mainLoop(self, window):
        actual_language = inter.actual_inter_language
        result = None
        self.outcome = None
        while not result:
            event, values = window.read()
            result = self.inputValidation(event=event, values=values, window=window, actual_language=actual_language)
            print(f"#092304u event: {event}, values: {values}")

    def createReturnSettings(self, values):
        """createas settings dict usable for option back end class to update self.__dict__"""

        print(f"#88888888888888888888888 radio value: {values['-AUS-1-0RADIO-']}")
        autosave_amount_type = inter.pieces if values["-AUS-1-1RADIO-"] else inter.days
        disabled_folder_usage = "ind" if values["-RADIO_1-RADIO-"] else "std"
        settings = {"main_folder": values["-PFL-IEX729X"], "standard_main_folder": values["-SFL-IEX729X"],
                    "result_folder": values["-RFL-IEX729X"], "autosave_folder": values["-AsFL-IEX729X"],
                    "autosave_amount": values["-AUS-2-"], "autosave_amount_type": autosave_amount_type,
                    "language": values["-LANGUAGE-"][0], "disabled_folder_usage": disabled_folder_usage,
                    "autosave_handling": values["-AUTO-S-2-RADIO-"]}
        return settings

    def optionWindow(self, settings: dict):
        layout = self._completeOptionWindowLayout(**settings)  #
        window = sg.Window(title=inter.options, layout=layout)
        self.mainLoop(window=window)
        window.close()
        if self.outcome:
            return self.createReturnSettings(self.outcome[1])


class Progressbar:
    blue_dotted_ring = b'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'

    # todo later: get some more progressbar b64

    def __init__(self, type_here="blue_dotted_ring", time_between_frames=50):

        self.time_between_frames = time_between_frames

        self.b64 = self.__class__.__dict__.get(type_here)
        self.visible = False
        self.alive = True
        self.queue = multiprocessing.Queue()
        self.process = self._jobProcess()

    def _createLayout(self):
        return [[sg.Image(data=self.b64, background_color='white', key="-PROGRESS-RING-")], ]

    def _createWindow(self):
        return sg.Window('My new window', self._createLayout(), no_titlebar=True, grab_anywhere=True, keep_on_top=True,
                         background_color='white', alpha_channel=.8, margins=(0, 0))

    def _updateAnimation(self, window: sg.Window):
        window["-PROGRESS-RING-"].update_animation(self.b64, self.time_between_frames)

    def _mainLoop(self):
        while self.alive:
            action = self.queue.get(block=True)
            if action == "start":
                window = self._createWindow()
                while self.alive:
                    try:
                        self.queue.get(block=False)
                        window.close()
                        break
                    except:
                        pass
                    _, _ = window.read(
                        timeout=10)  # loop every 10 ms to show that the 100 ms value below is used for animation
                    self._updateAnimation(window)
            elif action == "kill":
                return
            else:
                print(f"#09183432 lost queue put tact... ")

    def _jobProcess(self):
        process = multiprocessing.Process(target=self._mainLoop)
        process.start()
        return process

    def start(self):
        if not self.visible:
            print(f"#928374 shall start")
            self.queue.put("start")
            self.visible = True

    def stop(self):
        if self.visible:
            print(f"#928374 shall stop")
            self.queue.put("stop")
            self.visible = False

    def kill(self):
        print(f"#9212345 shall kill")
        [self.queue.put("kill") for _ in range(3)]


if __name__ == '__main__':
    start = datetime.datetime(*time.localtime()[:6])
    end = start + datetime.timedelta(days=8)
    task_here = task.Task(name="bk",
                          description="noch etwa, noch mehr, immer mehr mehr mehr emers",
                          start=start, end=end, priority=20)
    task_here.position = (2, 3)
    frame = TaskFrame(task_here)

    window = sg.Window("test", layout=[[frame]])

    for i in range(60, 260):

        window.read(timeout=1200)
        if i % 2 == 0:
            print(f"#9820932 chr:{i}: {chr(i)}")
            task_here.name = task_here.name + chr(i)
        else:
            task_here.name = task_here.name + "B"
        window[frame.key].Update(window)
    # while True:
    # task_button_creator = TaskFrameCreator()
    # button = task_button_creator.taskFrame(task_here)
    # buttonb = task_button_creator.emptyTaskFrame()
    # buttonc = task_button_creator.emptyTaskFrame()
    # buttond = task_button_creator.emptyTaskFrame()
    # buttone = task_button_creator.taskFrame(task_here)
    # buttonf = task_button_creator.emptyTaskFrame()
    # buttong = task_button_creator.emptyTaskFrame()
    # buttonh = task_button_creator.emptyTaskFrame()
    # buttoni = task_button_creator.taskFrame(task_here)
    # event, values = window.read()
    # print(F"#0823823 event: {event}; vlues: {values}")
    # window.close()
    # window = sg.Window("test", layout=[[button, buttonb, buttonc],
    #                                    [buttond, buttone, buttonf],
    #                                    [buttong, buttonh, buttoni]])
    #
    # win_creator = TaskInputWindowCreator()
    # event, values = win_creator.inputWindow(kind="Projekt", start=None)
    # print(event, values)

# if __name__ == '__main__':
#     progressbar = Progressbar(type_here="blue_dotted_ring")
#     progressbar.start()
#     time.sleep(1.5)
#     progressbar.stop()
#     time.sleep(1.5)
#
#     progressbar.start()
#     time.sleep(1.5)
#     progressbar.stop()
#     time.sleep(1.5)
#
#     progressbar.start()
#     time.sleep(1.5)
#     progressbar.kill()

# TODO ASAP fork or support PYSIMPPLEGUI


if __name__ == '__main__':
    pass
    # option = Option("save_option.bin")
    # gou_tools = MyGuiToolbox()
    # gou_tools.optionWindow(option.sSettings())
    # the option window asks folder for autosaves,
    # folder for result saves, it asks for us of an main project file and for the save folder for it,
    # but myby just for an standard project folder nested in documetation folder.
    # it asks for rules time based or amount based or none (no deletion) to care of autosave files.
    # return it

# if __name__ == '__main__':
#     start = datetime.datetime(*time.localtime()[:6])
#     end = start + datetime.timedelta(days=8)
#     task_here = task.Task(name="etwaesswoiihröiojwöoiefjmöoqweivjkmövvoiwjrvöoiwqerqs",
#                           description="noch etwa, noch mehr, immer mehr mehr mehr emers",
#                           start=start, end=end, priority=20)
#     task_here.position = (2, 3)
#     window = sg.Window("test", layout=[[sg.Text("etwas text")]])
#     window.read()
# while True:
# task_button_creator = TaskFrameCreator()
# button = task_button_creator.taskFrame(task_here)
# buttonb = task_button_creator.emptyTaskFrame()
# buttonc = task_button_creator.emptyTaskFrame()
# buttond = task_button_creator.emptyTaskFrame()
# buttone = task_button_creator.taskFrame(task_here)
# buttonf = task_button_creator.emptyTaskFrame()
# buttong = task_button_creator.emptyTaskFrame()
# buttonh = task_button_creator.emptyTaskFrame()
# buttoni = task_button_creator.taskFrame(task_here)
# event, values = window.read()
# print(F"#0823823 event: {event}; vlues: {values}")
# window.close()
# window = sg.Window("test", layout=[[button, buttonb, buttonc],
#                                    [buttond, buttone, buttonf],
#                                    [buttong, buttonh, buttoni]])
#
# win_creator = TaskInputWindowCreator()
# event, values = win_creator.inputWindow(kind="Projekt", start=None)
# print(event, values)


# if __name__ == '__main__':
# radio_one = RadioNew(text="rot", group_id="colors", default=True, background_color="#007700", enable_events=True)
# text_one = sg.Text(text="test text", background_color="#770000", #pad=(0,0)
#                    )
# radio_two = RadioNew(text="grün", group_id="colors", background_color="#007700", enable_events=True)
# text_two = sg.Text(text="test text", background_color="#770000", #pad=(75,55)
#                    )
# layout = [[radio_one, text_one], [radio_two, text_two]]
# window = sg.Window(title="My own Color Radios", layout=layout)
# event, values = window.read()
#
# # radio_one = RadioNew(text="rot", group_id="colors", default=True, background_color="#007700")
# text_one = sg.Text(text="test text", background_color="#770000", key=1 #pad=(0,0)
#                    )
# # radio_two = RadioNew(text="grün", group_id="colors", background_color="#007700")
# text_two = sg.Text(text="test text", background_color="#770000", key=2#pad=(75,55)
#                    )
# layout2 = [[text_one], [text_two]]
# window2 = sg.Window(title="My own Color Radios", layout=layout2)
# event2, values2 = window2.read()
