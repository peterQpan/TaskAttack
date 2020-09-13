__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"

import datetime
import multiprocessing
import os
import re
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

import b64_p_bars
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
    def okCancelLine(ok_button=inter.yes, cancel_button=inter.no,
                     key_ok="-OK-", key_cancel="-CANCEL-", left_padding=0):

        ok_button = sg.Button(button_text=ok_button, key=key_ok)
        cancel_button = sg.Button(button_text=cancel_button, key=key_cancel)
        if left_padding:
            padding = sg.Text(text=f"{' ' * left_padding}", key="-LEFT-PADDING-")
            return [padding, cancel_button, ok_button]
        return [cancel_button, ok_button]

    @staticmethod
    def yesNoPopup(title: str, text: str, ok_button=inter.yes, cancel_button=inter.no, size=(250, 70), keep_on_top=True,
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
                  MyGuiToolbox.okCancelLine(ok_button=ok_button, cancel_button=cancel_button,
                                            key_ok=key_ok, key_cancel=key_cancel)]
        window = sg.Window(title=title, layout=layout, auto_size_buttons=True, keep_on_top=keep_on_top, size=size)
        event, values = window.read()

        window.close()
        if event == key_ok:
            return True
        return False


    @staticmethod
    def webLinkDescriptionEnsurance(event, values, window):
        if event == '-SHORT_DESCRIPTIOM-':
            if len(values['-SHORT_DESCRIPTIOM-']) > 30:
                window['-SHORT_DESCRIPTIOM-'].update(values['-SHORT_DESCRIPTIOM-'][:-1])
            elif values['-SHORT_DESCRIPTIOM-'][-3:] == "<->":
                window['-SHORT_DESCRIPTIOM-'].update(values['-SHORT_DESCRIPTIOM-'][:-3])
        elif event == '-TEXT-INPUT-':
            print(f"#554545 event is text input: {event}")
            match = re.fullmatch(pattern=tools.webLinkRePattern(), string=window['-TEXT-INPUT-'].get())
            if match:
                print(f"#77777 match: {match}")
                window['-TEXT-INPUT-'].Update(text_color="#000000")
            else:
                window['-TEXT-INPUT-'].Update(text_color="#ff0000")

    @staticmethod
    def fileDescriptionEnsurance(event, values, window, *args, **kwargs):
        """
        takes care that short description dont gets longer than 30 figures
        and that not the file_name <-> short desciption seperator gets used by the user
        """
        if len(values['-SHORT_DESCRIPTIOM-']) > 30:
            window['-SHORT_DESCRIPTIOM-'].update(values['-SHORT_DESCRIPTIOM-'][:-1])
        elif values['-SHORT_DESCRIPTIOM-'][-3:] == "<->":
            window['-SHORT_DESCRIPTIOM-'].update(values['-SHORT_DESCRIPTIOM-'][:-3])



    @staticmethod
    def destinctTextWithDescriptionPopup(text_name: str, suggestet_text:str, description_name: str,
                                         suggested_description: str, ensuranc_function, *args, **kwargs):
        file_name_line = [sg.Text(text_name, size=(15, 1)),
                          sg.Input(default_text=suggestet_text, size=(50, 1), key='-TEXT-INPUT-', focus=True,
                                   enable_events=True)]
        description_line = [sg.Text(text=description_name, size=(15, 1)),
                            sg.Input(default_text=suggested_description, size=(50, 1), enable_events=True,
                                     key='-SHORT_DESCRIPTIOM-'), sg.Ok()]
        layout =  [file_name_line, description_line]

        window = sg.Window(title=inter.enter_weblink, layout=layout)
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, None):
                return False, False
            elif event == "Ok":
                main_output, short_description = window['-TEXT-INPUT-'].get(), window['-SHORT_DESCRIPTIOM-'].get()
                window.close()
                return main_output, short_description
            else:
                ensuranc_function(event=event, values=values, window=window)

    # user_defined_keys
    # next above: ("-PFL", "-RFL", "-AsFL")
    # under-keys: ("-DE", "-IEX729X", "-FB")

    # user_defined_keys
    # next above: ("-SFL")
    # under-keys: ("-DE", "-IEX729X", "-FB")


    # todo this time implement the opening in webbrowser if link is clicked

    # todo this time make globus a button menu, that gives the posibility to acess the links directly


class ResultFileCreator:



    def __init__(self):
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

    # @staticmethod
    # def _correctInputEnforcement(window, values):
    #     """
    #     takes care that short description dont gets longer than 30 figures
    #     and that not the file_name <-> short desciption seperator gets used by the user
    #     """
    #     if len(values['-SHORT_DESCRIPTIOM-']) > 30:
    #         window['-SHORT_DESCRIPTIOM-'].update(values['-SHORT_DESCRIPTIOM-'][:-1])
    #     elif values['-SHORT_DESCRIPTIOM-'][-3:] == "<->":
    #         window['-SHORT_DESCRIPTIOM-'].update(values['-SHORT_DESCRIPTIOM-'][:-3])
    #
    # def _newResultFilePopup(self, suggested_file_name: str, result_path: str,
    #                         kind_of_program: str, file_ext: str = ".ods"):
    #     """
    #     gets file_name and short file description for new task result file
    #     :return: filename, short_description
    #     """
    #     assert len(file_ext) == 4
    #     layout = self._newLayout(file_name=suggested_file_name, file_ext=file_ext, kind_of_program=kind_of_program,
    #                              result_path=result_path)
    #     window = sg.Window(title=inter.createResultFileTitle(kind_of_program=kind_of_program), layout=layout)
    #     while True:
    #         event, values = window.read()
    #         print(F"#099823 event: {event}; vlues: {values}")
    #         if event in (sg.WIN_CLOSED, None):
    #             return False, False
    #         elif event == '-SHORT_DESCRIPTIOM-':
    #             self._correctInputEnforcement(window=window, values=values)
    #         elif event == "Ok":  # could be else but for fast later additions withoutt trouble i will be very precise
    #             file_name, short_description = self._fetchResultFileParameters(
    #                 values=values, file_ext=file_ext, window=window)
    #             return file_name, short_description

    def _createAndOpenResultFile(self, kind_of_porogramm, file_path):
        template_file_path = self._file_templates[kind_of_porogramm][0]
        shutil.copy(tools.venvAbsPath(template_file_path), file_path)
        tools.openExternalFileSubPro(file_path=file_path)

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
            user_file_path, description = MyGuiToolbox.destinctTextWithDescriptionPopup(
                    text_name=inter.file_name, suggestet_text=suggested_file_name, description_name=inter.description,
                    suggested_description="", ensuranc_function=MyGuiToolbox.fileDescriptionEnsurance)
            # user_file_path, description = self._newResultFilePopup(
            #     suggested_file_name=suggested_file_name, result_path=result_path,
            #     kind_of_program=kind_of_porogramm, file_ext=self._file_templates[kind_of_porogramm][1], )

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
                if not MyGuiToolbox.yesNoPopup(title=inter.save_at, size=(None, None),
                                               text=f"{save_file_path}{inter.already_exists_override}"):
                    continue

            self._createAndOpenResultFile(kind_of_porogramm, save_file_path)
            task.addResultsFileAndDescription(save_file_path, description)
            break



class TaskFrame(sg.Frame):

    def __init__(self, task: task.Task = None, size=31, view="complete"):

        # self._button_menu_list = {"complete": inter.b_b_m_l, "partial":inter.c_b_m_l}[view]
        self.size = size

        if task:
            self.task = task
            self.key = F"-MY-TASK-FRAME-{str(self.task.sPosition())}"
            self.taskFrame()  # superMethod
        else:
            self.emptyTaskFrame()  # superMethod

    def sSize(self):
        """
        :return: int
        :type int
        """
        return self.size

    @staticmethod
    def nAIt(wantet_value):
        return "N.A." if not wantet_value else wantet_value

    def _toolTipText(self):
        """
        :return: full plain textual representation of an task.Task() suitable as tooltip_text
        """
        tt = ""
        tt += f"   {self.task.hierarchyTreePositionString()}\n\n"
        tt += f"   {self.task.sName()}\n\n"
        tt += f"   {inter.start}: {self.task.sStart()}   {inter.end}:v{self.nAIt(self.task.sEnde())}   {inter.priority}: {self.task.sPriority()}   \n"
        tt += f"   {inter.rem_days}:..................................... {self.nAIt(self.task.sRemainingDays())}   \n"
        tt += f"   {inter.project_part_percentage}:............... {self.task.sPercentage()}%   \n"
        tt += f"   {inter.sub_task_amount}:............................... {len(self.task.sSubTasks()) if self.task.sSubTasks() else '0'}   \n"
        tt += f"   {inter.percent_compled}:............................. {self.task.sCompleted():5.1f}%   \n\n"
        tt += "    \n   ".join(textwrap.wrap(self.task.sDescription(), width=90))

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

    # def sOptionButtonMenuList(self):
    #     """
    #     :return: list of list, sg.ButtonMenu.layout for option button menu
    #     """
    #     return self._button_menu_list

    def _buttonLinePlaceHolder(self, background_color, padding_size):
        # origiinal x_size: self.sSize() - 15
        return sg.Text(text="", size=(padding_size, 1), background_color=background_color)


    def _createButtonMenuWithResultFileEntrys(self, button_menu_list):
        results = self.task.sResults()

        if results:
            for file_path, short_description in results:
                if short_description:
                    line = f"{short_description} <-> {file_path}"
                else:
                    line = f"{file_path}"
                button_menu_list[1][5].append(line)
            return button_menu_list, True
        else:
            return button_menu_list, False

    def _createButtonMenuWithWebLinkEntrys(self, button_menu_list):
        web_links = self.task.sWebLinks()
        if web_links:
            for web_link, short_description in web_links:
                if short_description:
                    line = f"{short_description} <-> {web_link}"
                else:
                    line = f"{web_link}"
                button_menu_list[1][8].append(line)
            return button_menu_list, True
        else:
            return button_menu_list, False

    def _buttonMenuLine(self, background_color):
        """
        :return: option menu button for every task frame
        """
        button_menu_list = deepcopy(inter.basic_button_menu)

        button_menu_list, file_flag = self._createButtonMenuWithResultFileEntrys(button_menu_list)
        button_menu_list, link_flag = self._createButtonMenuWithWebLinkEntrys(button_menu_list)

        target_image = sg.Image(filename="templates/crosshair_black.png", enable_events=True, key=f"-TARGET-#7#{self.task.sPosition()}")
        file_image = sg.Image(filename="templates/file.png") if file_flag else None
        globe_image = sg.Image(filename="templates/globus.png") if link_flag else None

        #todo modularize this
        if file_image and globe_image:
            placeholer = self._buttonLinePlaceHolder(background_color=background_color, padding_size=self.sSize() - 30)
            option_button = sg.ButtonMenu(button_text=inter.options, menu_def=button_menu_list,
                                          key=f'-BMENU-#7#{self.task.sPosition()}')

            return [target_image, placeholer, globe_image, file_image, option_button]
        elif file_image:

            placeholer = self._buttonLinePlaceHolder(background_color=background_color, padding_size=self.sSize() - 25)
            option_button = sg.ButtonMenu(button_text=inter.options, menu_def=button_menu_list,
                                          key=f'-BMENU-#7#{self.task.sPosition()}')

            return [target_image, placeholer, file_image, option_button]
        elif globe_image:

            placeholer = self._buttonLinePlaceHolder(background_color=background_color, padding_size=self.sSize() - 25)
            option_button = sg.ButtonMenu(button_text=inter.options, menu_def=button_menu_list,
                                          key=f'-BMENU-#7#{self.task.sPosition()}')

            return [target_image, placeholer, globe_image, option_button]
        else:
            placeholder = self._buttonLinePlaceHolder(background_color=background_color, padding_size=self.sSize() - 20)
            option_button = sg.ButtonMenu(button_text=inter.options, menu_def=inter.basic_button_menu,
                                          key=f'-BMENU-#7#{self.task.sPosition()}')
            return [target_image, placeholder, option_button]

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
                                        tooltip=tooltip_text, background_color=frame_color, key=self.key, )

    def taskFrame(self):
        """
        :return: sg.Frame which represents the short Tree notation of an Task inclusive a full tooltip text
        """
        tooltip_text = self._toolTipText()
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
        # todo think is it really smart to refer to elements by using sg.window[key] instead of make all elements
        #  part of self and update them by self.element.Update ??
        """overriding of method wich enables the direct window[key] access
        and passes it along to the containing elements"""
        tooltip_text = self._toolTipText()
        background_color = self.task.taskDeadlineColor()
        frame_name = self.task.hierarchyTreePositionString()

        print(f"#09288309u parentWindow: {self.ParentWindow}")
        self._updateFixedElements(window=window, background_color=background_color, tooltip_text=tooltip_text)
        self._updateChangingElements(window=window, background_color=background_color, tooltip_text=tooltip_text)

        super(TaskFrame, self).Update(value=frame_name)
        self.SetTooltip(tooltip_text=tooltip_text)

    def _priorityCompletedLine(self, tooltip_text, background_color, ):
        priority_sg_object = sg.Text(text=f"{inter.short_pr}:.{self.task.sPriority():3d}", tooltip=tooltip_text,
                                     background_color=background_color, key=f"{self.key}PRIORITY-")
        completed_sg_object = self._isCompletedElement(self.task, tooltip_text=tooltip_text,
                                                       background_color=background_color)
        return [priority_sg_object, completed_sg_object]

    def activateTarget(self):
        self.target_image.Update(filename="templates/crosshair_white.png", size=(26,26))

    def deActivateTarget(self):
        self.target_image.Update(filename="templates/crosshair_black.png", size=(26,26))


class TaskInputWindowCreator:

    # todo think should this not too a class of its own instead of an factory?!?
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
                MyGuiToolbox().okCancelLine(ok_button=inter.ok, cancel_button=inter.cancel,
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
        if event == "-RADIO_1-RADIO-":
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

    def __init__(self, type_here="blue_loading_bar", time_between_frames=30):

        self.time_between_frames = time_between_frames

        self.b64 = b64_p_bars.__dict__.get(type_here)
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
