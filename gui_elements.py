__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"

import datetime
import os
import shutil
import textwrap
import threading
import time
from copy import deepcopy
from time import strftime

import PySimpleGUI as sg
from nose.util import file_like

import task
import tools
from internationalisation import inter
from tools import nowDateTime


class RadioNew(sg.Frame):
    #todo ready to use but try to optimize by using
    """
    New because its Text isuneatable
    Radio Button Element - Used in a group of other Radio Elements to provide user with ability to select only
    1 choice in a list of choices.
    """

    def __init__(self, text, group_id, default=False, disabled=False, text_size=(None,None), rad_size= (None, None),
                 auto_size_text=None, background_color=None, text_color=None, font=None, key=None, rad_pad=(0,0),
                 text_pad=(0,0), pad=None,
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
                              font=font, key=self.radio_key, pad=rad_pad, tooltip=tooltip, change_submits=change_submits,
                              enable_events=enable_events, visible=visible, metadata=metadata)
        self.text_key = f"{key}TEXT-"
        self.text = sg.Text(text=text, size=text_size, auto_size_text=auto_size_text, click_submits=click_submits,
                            enable_events=enable_events, relief=relief, font=font, text_color=text_color,
                            background_color=background_color, border_width=border_width, justification=justification,
                            pad=text_pad, key=self.text_key, right_click_menu=right_click_menu, tooltip=tooltip,
                            visible=visible, metadata=metadata)
        self.layout = [[self.radio, self.text]]
        super().__init__(title="", layout=self.layout, relief=sg.RELIEF_FLAT, font=font, pad=pad,
                         border_width=border_width, key=key, tooltip=tooltip, right_click_menu=right_click_menu,
                         visible=visible, element_justification=element_justification, metadata=metadata)

    def Update(self, text=None, background_color=None, text_color=None, font=None, radio_value=None, disabled=None, visible=None):
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
        self.text.Update(value=text, background_color=background_color, text_color=text_color, font=font, visible=visible)
        self.radio.Update(value=radio_value, disabled=disabled, visible=visible)
        super().Update(visible=visible)


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

class MyGuiToolbox:

    @staticmethod
    def _okCancelLine(ok_button=inter.yes, cancel_button=inter.no,
                      key_ok="-OK-", key_candel="-CANCEL-", left_padding=0):

        ok_button = sg.Button(button_text=ok_button, key=key_ok)
        cancel_button = sg.Button(button_text=cancel_button, key=key_candel)
        if left_padding:
            padding = sg.Text(text=f"{' ' * left_padding}")
            return [padding, cancel_button, ok_button]
        return [cancel_button, ok_button]

    @staticmethod
    def YesNoPopup(title:str, text:str, ok_button=inter.yes, cancel_button=inter.no, size=(250, 70), keep_on_top=True,
                   key_ok="-OK-", key_candel="-CANCEL-", *args, **kwargs):
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
                  MyGuiToolbox._okCancelLine(ok_button=ok_button, cancel_button=cancel_button,
                                             key_ok="-OK-", key_candel="-CANCEL-")]
        window = sg.Window(title=title, layout=layout, auto_size_buttons=True, keep_on_top=keep_on_top, size=size)
        event, values = window.read()
        print(F"#092976o23 event: {event}; vlues: {values}")

        window.close()
        if event == ok_button:
            return True
        return False

    #user_defined_keys
    #next above: ("-PFL", "-RFL", "-AsFL")
    #under-keys: ("-DE", "-IE", "-FB")



    #user_defined_keys
    #next above: ("-SFL")
    #under-keys: ("-DE", "-IE", "-FB")




    def _setDisabledStatusToUserDirectoryFrame(self, window:sg.Window, disabled:bool):
        """option-window
        sets user directory choice frame text in red or green and buttons enabled and disabled
        :param window: option_window
        :param disabled: bool is true if user chooses to make distinct saving directory
        frame key:
        next above: ("-PFL", "-RFL", "-AsFL")
        under-keys: ("-DE":color, "-IE":disabled, "-FB":disabled)

        """
        text_color = "#ff0000" if disabled else "#00ff00"
        for first_part in ("-PFL", "-RFL", "-AsFL"):
            window[f"{first_part}-DE"].Update(text_color=text_color)
            window[f"{first_part}-IE"].Update(disabled=disabled)
            window[f"{first_part}-FB"].Update(disabled=disabled)

    def _setDisabledStatusToStandardDirectoryFrame(self, window:sg.Window, disabled:bool):
        """option-window
        sets standard directory choice frame text in red or green and buttons enabled and disabled
        :param window: option_window
        :param disabled: bool is true if user chooses to make standard saving directory
        next above: ("-SFL")
        under-keys: ("-DE":color, "-IE":disabled, "-FB":disabled)
        """
        text_color = "#ff0000" if disabled else "#00ff00"
        window["-SFL-DE"].Update(text_color=text_color)
        window["-SFL-IE"].Update(disabled=disabled)
        window["-SFL-FB"].Update(disabled=disabled)

    def _horizontalRadioChoiceFrame(self, all_types:tuple, active_type, disabled, key:str, group_id="dura_radio"):
        """option-window
        makes a horizontal radio button group
        :param all_types: tuple of all values
        :param active_type: value which is supposed to be active
        :param disabled: needed if elements are supposed to be enablede
        :return: sg.Frame()
        """
        layout = []
        for index, d_type in enumerate(all_types):
            if d_type == active_type:
                radio_button = RadioNew(text=d_type, group_id=group_id, default=True, disabled=disabled, key=f"{key}{index}")
            else:
                radio_button = RadioNew(text=d_type, group_id=group_id, default=False, disabled=disabled, key=f"{key}{index}")
            layout.append([radio_button])
        print(f"layout0283u: {layout}")
        frame = sg.Frame(title="", relief=sg.RELIEF_FLAT, layout=layout, pad=(0,0))
        return frame

    def _setDurationRadiosWithNewLanguage(self, all_types:tuple, key:str, window):
        """option-window
        makes a horizontal radio button group
        :param all_types: tuple of all values
        :param active_type: value which is supposed to be active
        :param disabled: needed if elements are supposed to be enablede
        :return: sg.Frame()
        """
        for index, d_type in enumerate(all_types):
            window[f"{key}{index}"].Update(text=d_type)


    def autoSaveSettingInputFrame(self, duration_type:str, duration:int, disabled:bool, enable_radio_button:sg.Radio):
        """option-window
        frame for auto save file handeling setting"
        :param duration_type: inter.days or inter.pieces indicates actual settings
        :param duration: actual duration setting
        :param disabled: True if no auto save handeln
        :param enable_radio_button: sg.Radio()
        :return: sg.Frame
        """
        duration_type_radio_frame = self._horizontalRadioChoiceFrame(all_types=inter.duration_types, active_type=duration_type, disabled=disabled, key="-AUS-1-")
        duration_entry = sg.Input(default_text=duration, disabled=disabled, enable_events=True, size=(4, 1), key="-AUS-2-") #todo change in double radio frame
        layout = [[enable_radio_button, duration_entry, duration_type_radio_frame]]
        print(f"layout1113u: {layout}")
        frame = sg.Frame(title="", layout=layout, relief=sg.RELIEF_FLAT, pad=(0,0))
        return frame

    @staticmethod
    def _setImputAutoSaveFrame(window, disabled):
        window["-AUS-1-0"].Update(disabled=disabled)
        window["-AUS-1-1"].Update(disabled=disabled)
        window["-AUS-2-"].Update(disabled=disabled)




    def _autoSaveFileHandlingRulesFrame(self, duration_type:str, duration:int, autosave_handeling:bool):
        """option-window
        complete frame for auto save file handling
        :param duration_type: inter.days or inter.pieces indicates actual settings
        :param duration: actual duration setting
        :param autosave_handeling: actual setting, True if auto save files are handeled
        :return: layout line: [sg.frame]
        """
        no_auto_save_handling_radio_b = RadioNew(
                text=inter.no_autosave_deletion, group_id="autosave_deletion", default=(not autosave_handeling),
                enable_events=True, text_size=(30,1), key="-AUTO-S-1-")
        auto_save_handeling_radio_b = RadioNew(
                text=inter.autosave_deletion, group_id="autosave_deletion", default=autosave_handeling,
                enable_events=True, text_size=(30,1 ), key="-AUTO-S-2-")
        auto_save_setting_frame = self.autoSaveSettingInputFrame(
                duration_type=duration_type, duration=duration, disabled=(not autosave_handeling),
                enable_radio_button=auto_save_handeling_radio_b)
        layout = [[no_auto_save_handling_radio_b], [auto_save_setting_frame]]
        print(f"layout 84652: {layout}")

        frame = sg.Frame(title="", layout=layout)
        return [frame]

    def _folderLine(self, name:str, directory:file_like, disabled:bool, key):
        """option-window
        creates a folder input line [sg.Text, sg.Input, sg.FolderBrowse]
        :param name: line description
        :param directory: actual directory
        :param disabled: disables complete line
        :param key: master_key for this line, becomes sub keys: -DE, -IE, -FB
        :return: layout line: [sg.Text, sg.Input, sg.FolderBrowse]
        """
        text_color = "#ff0000" if disabled else "#00ff00"
        directory = directory if directory else ""
        description_elemetn = sg.Text(text=name, size=(15, 1), text_color=text_color, key=f"{key}-DE")
        input_element = sg.Input(default_text=directory, size=[25, 1], disabled=disabled, key=f"{key}-IE", )
        folder_button = sg.FolderBrowse(button_text=inter.browse, disabled=disabled, key=f"{key}-FB")

        return [description_elemetn, input_element, folder_button]

    def _userDefinedFolderStructureFrame(self, directorys:tuple, disabled):
        """option-window
        Frame for user commanded save directory structure
        :param directorys: directorys for (*.tak, results, autosave.tak
        :param disabled: disabled if standard folder structure is used
        :return: sg.Frame
        """
        user_decission_element_ind = RadioNew(
                text=inter.own_folder_setup, group_id="folder_setup", enable_events=True, default=(not disabled),
                key="-RADIO_2-")

        project_folder_line = self._folderLine(name = inter.project_folder, disabled=disabled, directory=directorys[0], key="-PFL")
        result_folder_line = self._folderLine(name=inter.results_folder, disabled=disabled, directory=directorys[1], key="-RFL")
        autosave_folder_line = self._folderLine(name=inter.auto_save_folder, disabled=disabled, directory=directorys[2], key="-AsFL")

        layout = [[user_decission_element_ind], project_folder_line, result_folder_line, autosave_folder_line]
        print(f"layout 54wergs: {layout}")

        return sg.Frame(title="", layout=layout, relief=sg.RELIEF_FLAT)

    def _standardFolderStructureFrame(self, directorys, disabled):
        """option-window
        Frame for user commanded save directory structure
        :param directorys: directorys for (*.tak, results, autosave.tak
        :param disabled: disabled if standard folder structure is used
        :return: sg.Frame
        """

        user_decission_element_std = RadioNew(
                text=inter.standard_folder_setup, group_id="folder_setup", enable_events=True, default=(not disabled),
                key="-RADIO_1-")

        project_folder_line = self._folderLine(name = inter.project_folder, disabled=disabled, directory=directorys[0], key="-SFL")
        placeholder_line_one = [sg.Text(text="", pad=(5,7))]
        placeholder_line_two = [sg.Text(text="", pad=(5,7))]


        layout = [[user_decission_element_std], project_folder_line, placeholder_line_one, placeholder_line_two]
        print(f"layout qwsdfsd: {layout}")

        return sg.Frame(title="", layout=layout, relief=sg.RELIEF_FLAT)

    def _FolderStuchturLayoutLine(self, directorys:tuple, wich_disabled:str):
        """optioln-window
        complete save folder line, standard AND user decided
        :param directorys: actual folders
        :param wich_enabled: "ind" or "std"
        :return: complete save folder line: [sg.Frame]
        """

        if wich_disabled == "ind":
            layout = [[self._standardFolderStructureFrame(directorys=directorys, disabled=True),
                    self._userDefinedFolderStructureFrame(directorys=directorys, disabled=False)]]
        else:
            layout = [[self._standardFolderStructureFrame(directorys=directorys, disabled=False),
                    self._userDefinedFolderStructureFrame(directorys=directorys, disabled=True)]]
        folder_structur_line = sg.Frame(title="", layout=layout)
        return [folder_structur_line]

    def _languageTextFrame(self):
        """option-window
        creates an frame three elements high to match listbox in height and align accordingly
        :return: sg.Frame
        """
        layout = [[sg.Text(text=f"{inter.language}     ", key="language-t-f", size=(10,1))], [sg.Text()], [sg.Text()]]
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
        language_selection_List_box = sg.Listbox(values=inter.sLanguages(), default_values=actual_language,
                                                 size=(10, 4),
                                                 enable_events=True, key="-LANGUAGE-")
        return [language_text_frame, language_selection_List_box]

    def _completeOptionWindowLayout(self, directorys:tuple, disabled_directory_mode:str, actual_language:str,
                                    autosave_handling:bool, duration_type:str, duration:int):
        """option-window
        gathers all lines together ond creates final layout line
        :param directorys: achtual_directorys
        :param disabled_directory_mode: "ind" or "std" --> individual - standard
        :param actual_language: 
        :param autosave_handling: if auto save handling
        :param duration_type: actualy set duration type inter.days or inter.pieces
        :param duration: actualy set duration amount
        :return: final layout line [self.line, self.line, self.line]
        """
        return [self._languageSettingsLine(actual_language),
                self._FolderStuchturLayoutLine(directorys=directorys, wich_disabled=disabled_directory_mode),
                self._autoSaveFileHandlingRulesFrame(
                        duration_type=duration_type, duration=duration, autosave_handeling=autosave_handling),
                self._okCancelLine(ok_button=inter.ok, cancel_button=inter.cancel, left_padding=163)]

    def optionWindow(self):

        directorys = ("/home/ich/Dokumente", None, None)
        wich_disabled = "ind"
        actual_language = "deutsch"
        duration_type = inter.days
        duration = 10
        autosave_handling = True

        layout = self._completeOptionWindowLayout(
                directorys=directorys, disabled_directory_mode=wich_disabled, actual_language=actual_language,
                duration_type=duration_type, duration=duration, autosave_handling=autosave_handling)#
        print(f"layout sfd45: {layout}")

        window = sg.Window(title=inter.options, layout=layout)
        while True:
            event, values = window.read()
            if event == "-RADIO_1-":
                self._setDisabledStatusToStandardDirectoryFrame(window=window, disabled=False)
                self._setDisabledStatusToUserDirectoryFrame(window=window, disabled=True)

            elif event == "-RADIO_2-":
                self._setDisabledStatusToStandardDirectoryFrame(window=window, disabled=True)
                self._setDisabledStatusToUserDirectoryFrame(window=window, disabled=False)

            elif event == "-AUTO-S-1-":
                self._setImputAutoSaveFrame(window=window, disabled=True)
            elif event == "-AUTO-S-2-":
                self._setImputAutoSaveFrame(window=window, disabled=False)
            elif event == "-LANGUAGE-":
                choosen_language = values[event][0]
                print(f"choosen language: {choosen_language}")
                language = inter.language
                inter.setLanguage(choosen_language)
                for key, text in {"-PFL": inter.project_folder, "-RFL":inter.results, "-AsFL":inter.auto_save_folder}. items():
                    print(f"key 0932u5: {key}-DE")
                    window[f"{key}-DE"].Update(value=text)
                    # sg.Text.Update(value=text)
                window[f"-SFL-DE"].Update(value=inter.project_folder)
                window["language-t-f"].Update(value=inter.language)
                window["-RADIO_1-"].Update(text=inter.standard_folder_setup)
                window["-RADIO_2-"].Update(text=inter.own_folder_setup)
                self._setDurationRadiosWithNewLanguage(all_types=inter.duration_types, key="-AUS-1-", window=window)
                window["-AUTO-S-1-"].Update(text=inter.no_autosave_deletion)
                window["-AUTO-S-2-"].Update(text=inter.autosave_deletion)
                window["-CANCEL-"].Update(text=inter.cancel)
                # sg.Button.Update()
            print(f"#io3409283lkjnk event: {event}, values: {values}")


#fixme make my own radio buttons because you cant update text of radiobuttons MAYBE Fork PYSIMPLEGUI OR GO AS SUPPORTER

#TODO ASAP fork or support PYSIMPPLEGUI


if __name__ == '__main__':
    gou_tools = MyGuiToolbox()
    gou_tools.optionWindow()
    # the option window asks folder for autosaves,
    # folder for result saves, it asks for us of an main project file and for the save folder for it,
    # but myby just for an standard project folder nested in documetation folder.
    # it asks for rules time based or amount based or none (no deletion) to care of autosave files.
    # return it



class ResultFileCreator:

    def __init__(self):
        #self._external_threads = []
        self._file_templates = {inter.writer:("/templates/writer_template.odt", ".odt"),
                                inter.spreadsheet:("/templates/spreadsheet_template.ods", ".ods"),
                                inter.presentation:("/templates/presentation_template.odp", ".odp"),
                                inter.drawing:("/templates/drawing_template.odg", ".odg"),
                                inter.database:("/templates/database_template.odb", ".odb"),
                                inter.gimp:("/templates/gimp_template.xcf", ".xcf"),
                                inter.svg:("/templates/inkscape_template.svg", ".svg")}

    def _newLayout(self, file_name, file_ext, kind_of_program):
        """creates new layout for file name / save as; short descripton pop up window"""
        file_name_line =[sg.Text(inter.file_name, size=(15, 1)),
                  sg.Input(default_text=f"{file_name}{file_ext}", size=(30, 1), key='-FILE-NAME-'),
                  sg.FileSaveAs(inter.save_at, file_types=((kind_of_program, file_ext),))]
        description_line = [sg.Text(inter.short_description, size=(15, 1)),
                  sg.Input(size=(30, 1), enable_events=True, key='-SHORT_DESCRIPTIOM-', focus=True),
                  sg.Ok()]
        return [file_name_line, description_line]

    def _correctInputEnforcement(self, window, values):
        """
        takes care that short description dont gets longer than 30 figures
        and that not the file_name <-> short desciption seperator gets used by the user
        """
        if len(values['-SHORT_DESCRIPTIOM-']) > 30:
            window['-SHORT_DESCRIPTIOM-'].update(values['-SHORT_DESCRIPTIOM-'][:-1])
        elif values['-SHORT_DESCRIPTIOM-'][-3:] == "<->":
            window['-SHORT_DESCRIPTIOM-'].update(values['-SHORT_DESCRIPTIOM-'][:-3])

    def _newResultFilePopup(self, file_name: str, kind_of_program: str, file_ext: str = ".ods"):
        """
        gets file_name and short file description for new task result file
        :return: filename, short_description
        """
        assert len(file_ext) == 4
        layout = self._newLayout(file_name=file_name, file_ext=file_ext, kind_of_program=kind_of_program)
        window = sg.Window(title=inter.createResultFileTitle(kind_of_program=kind_of_program) , layout=layout)
        while True:
            event, values = window.read()
            print(F"#099823 event: {event}; vlues: {values}")
            if event is None:
                return None
            elif event == '-SHORT_DESCRIPTIOM-':
                self._correctInputEnforcement(window=window, values=values)
            elif event == "Ok":  # could be else but for fast later additions withoutt trouble i will be very precise
                file_name, short_description = self._fetchResultFileParameters(
                        values=values, file_ext=file_ext, window=window)
                return file_name, short_description

    def _copyFileTemplateAndOpenExternalApplicationToEditIt(self, kind_of_porogramm, file_path):
        template_file_path = self._file_templates[kind_of_porogramm][0]
        # todo make an documents folder-project-save-structure
        shutil.copy(tools.venvAbsPath(template_file_path), file_path)
        tools.openExternalFile(file_path=file_path  #, threads=self._external_threads
                               )

    def _createSuggestingTaskFileName(self, task):
        """
        creats a suggested task filename depending on task name, project name, date and time
        :return :str file_name
        """
        nameing_list = task.hierarchyTreePositionList()
        nowtime_str = str(nowDateTime()).replace(" ", "_")
        return f"{nowtime_str}_{nameing_list[0]}_{nameing_list[-1]}"

    def _fetchResultFileParameters(self, values, file_ext, window):
        """gets filename and short description from popup window and returns it"""
        file_name = values['-FILE-NAME-']
        file_path = tools.completeFilePathWithExtension(file_name, file_ext)
        short_description = values['-SHORT_DESCRIPTIOM-']
        window.close()
        return file_path, short_description

    def newResultFile(self, task:task.Task, kind_of_porogramm):
        """
        creates new result file
        :param kind_of_porogramm: inter.presentation, inter.spreadsheet, etc...
        """
        file_name = self._createSuggestingTaskFileName(task)
        while True:
            try:
                file_path, short_description = self._newResultFilePopup(
                        file_name=file_name, kind_of_program=kind_of_porogramm, file_ext=self._file_templates[kind_of_porogramm][1])
            except TypeError:
                break
            if os.path.exists(file_path):
                if not MyGuiToolbox.YesNoPopup(title=inter.save_at, text=inter.allready_exists_override):
                    continue
            self._copyFileTemplateAndOpenExternalApplicationToEditIt(kind_of_porogramm, file_path)
            task.addResultsFileAndDescription(file_path, short_description)
            break


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

    def _basicTaskFrame(self, frame_name:str, name_line:list, priority, completed, option_button_line:list,
                        relief=sg.RELIEF_RAISED, tooltip_text:str="", frame_color:str=None):
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
        #origiinal x_size: self.sSize() - 15
        return sg.Text(text="", size=(padding_size,1), background_color=background_color)


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
            placeholer = self._buttonLinePlaceHolder(background_color=background_color, padding_size=self.sSize()-20)
            image = sg.Image(filename="templates/file.png")
            option_button = sg.ButtonMenu(button_text=inter.options, menu_def=result_file_button_menu, key=f'-BMENU-#7#{task.sPosition()}')

            return  [placeholer, image, option_button]

        else:
            placeholder = self._buttonLinePlaceHolder(background_color=background_color, padding_size=self.sSize()-15)
            option_button = sg.ButtonMenu(button_text=inter.options, menu_def=self.sOptionButtonMenuList(), key=f'-BMENU-#7#{task.sPosition()}')
            return [placeholder, option_button]




    def taskFrame(self, task:task.Task):
        """
        :return: sg.Frame which represents the short Tree notation of an Task inclusive a full tooltip text
        """
        tooltip_text = self._toolTipText(task)
        background_color = task.taskDeadlineColor()

        name_line = self._nameLine(task=task, tooltip_text=tooltip_text, background_color=background_color)
        priority_sg_object = sg.Text(text=f"{inter.short_pr}:.{task.sPriority():3d}", tooltip=tooltip_text, background_color=background_color)
        completed_sg_object = self._isCompletedElement(task, tooltip_text=tooltip_text, background_color=background_color)

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
            print(F"#897868912 event: {event}; vlues: {values}")

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
                sg.Spin(values=[0,1,2,3,4,5,6,7,8,9], initial_value=inital_value,
                        size=(2,1), key='priority', enable_events=True),
                sg.Text(key='priority-KORREKTUR-', text_color="#FF0000", size=(35, 1))]
                # sg.InputText(default_text=priority, key='priority', enable_events=True)]

    def _calenderLine(self, calendar_date:datetime.datetime, s_or_e=inter.start, key='-START_BUTTON-', target='-START_BUTTON-'):
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

    def _calendarButtonParameter(self, calendar_date:datetime.datetime=None, s_or_e=inter.start):
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


if __name__ == '__main__':
    start = datetime.datetime(*time.localtime()[:6])
    end = start + datetime.timedelta(days=8)
    task_here = task.Task(name="etwaesswoiihröiojwöoiefjmöoqweivjkmövvoiwjrvöoiwqerqs",
                          description="noch etwa, noch mehr, immer mehr mehr mehr emers",
                          start=start, end=end, priority=20)
    task_here.position = (2,3)
    window = sg.Window("test", layout=[[sg.Text("etwas text")]])
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

