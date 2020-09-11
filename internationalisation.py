__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"


class Internationalisation:
    def __init__(self, language:str=None):
        self.languages = {"de": "deutsch", "en": "english"}
        self.actual_inter_language = language
        self.setLanguage(language=language)
        self.left_pading_amounts = {"deutsch": 149, "english":168}


    def sLanguages(self):
        return sorted(self.languages.values())

    def sLanguageAbbreviations(self):
        return self.languages.keys()

    def sLanguageAbreviationMapping(self):
        return self.languages

    def setLanguage(self, language):
        self.actual_inter_language =language
        {"deutsch":self._setGerman, "english": self._setEnglish}[language]()

    def sActualLanguage(self):
        return self.actual_inter_language

    def _setGerman(self):
        # Buttons
        self.yes = "Ja"
        self.no = "Nein"
        self.start = "Start"
        self.end = "Ende"
        self.options = "Optionen"
        self.ok = "Übernehmen"
        self.cancel = "Abbrechen"
        self.browse = "Browse"

        self.own_folder_setup = "Eigene Ordner Strucktur"
        self.standard_folder_setup = "Standard Ordner"




        # Menu entries
        self.file = "Datei"
        self.new_project_sheet = "Neue Projekt Tabelle"
        self.open = "Öffnen"
        self.save = "Speichern"
        self.save_at = "Speichern in"
        self.exit = "Beenden"

        self.project = "Projekt"
        self.new_project = "Neues Projekt"

        self.edit = "Bearbeiten"
        self.restore_task = "Aufgabe widerherstellen"

        self.settings = "Einstellungen"


        self.window = "Fenster"
        self.reload = "Neu laden"
        self.help = "Hilfe"
        self.about = "Über..."

        self.sub_task = 'Unteraufgabe'
        self.compose_results = "Verfasse Ergebnisse"
        self.results = "Ergebnisse"

        self.isolate = "Isolieren"
        self.delete = "Löschen"
        self.paste = "Einfügen"
        self.cut = "Ausschneiden"
        self.copy = "Kopieren"
        self.tree_view = "Gesammtansicht"

        self.writer = "Text"
        self.spreadsheet = "Tabellenkalkulation"
        self.presentation = "Präsentation"
        self.database = "Datenbank"
        self.drawing = "Office-Zeichnung"
        self.gimp = "Pixel-Grafik"
        self.svg = "Vektor-Grafik"


        # texts
        self.projects = "Projekte"
        self.realy_delete = "Wirklich löschen"
        self.open_project = "Offenes Projekt"
        self.priority = "Priorität"
        self.low = "low"
        self.high = "high"

        self.short_pr = "PR"
        self.rem_days = "Verbleibende Tage"
        self.project_part_percentage = "Prozentualer Anteil am gesamt Projekt"
        self.sub_task_amount = "Anzahl Unteraufgaben"
        self.percent_compled = "Vollendet in Prozent"
        self.completed = "Vollendet"
        self.not_later_than_master = "Nicht später als Master-Task"
        self.really_less_important_than_master = "Wirklich unwichtiger als Master-Task?!?"

        self.description = "Beschreibung"
        self.task = "Aufgabe"
        self.app_name = "TaskAttack Projekt und Taskmanager"
        self.file_name = "Dateiname"
        self.short_description = "Kurzbeschreibung"

        self.project_folder = "Projekt Ordner"
        self.results_folder = "Ergebnisse"
        self.auto_save_folder =  "Autospeichern"

        self.language = "Sprache"
        self.days = "Tage"
        self.pieces = "Stück"

        self.no_autosave_deletion = "Kein Löschen der Autospeicherdateien"
        self.autosave_deletion = "Autospeicherdateien löschen bis auf"
        self.already_exists_override = "\nbesteht bereits!!!\nÜberschreiben?"



    def _setEnglish(self):
        # Buttons
        self.yes = "Yes"
        self.no = "No"
        self.start = "Start"
        self.end = "End"
        self.options = "Options"
        self.ok = "OK"
        self.cancel = "Cancel"
        self.browse = "Browse"

        self.own_folder_setup = "Own folder setup"
        self.standard_folder_setup = "Standard folders"

        # Menu entries
        self.file = "File"
        self.new_project_sheet = "New Project Sheet"
        self.open = "Open"
        self.save = "Save"
        self.save_at = "Save at"
        self.exit = "Exit"

        self.project = "Project"
        self.new_project = "New Project"

        self.edit = "Edit"
        self.restore_task = "Restore Task"

        self.settings = "Settings"

        self.window = "Window"
        self.reload = "Reload"
        self.help = "Help"
        self.about = "About..."

        self.sub_task = 'Subtask'
        self.compose_results = "Compose result"
        self.results = "Results"
        self.isolate = "Isolate"
        self.delete = "Delete"
        self.paste = "Paste"
        self.cut = "Cut"
        self.copy = "Copy"
        self.tree_view = "Tree view"

        self.writer = "Writer"
        self.spreadsheet = "Spreadsheet"
        self.presentation = "Presentation"
        self.database = "Database"
        self.drawing = "Drawing"
        self.gimp = "Pixel-Manipulation"
        self.svg = "Vektor-Manipulation"

        # texts
        self.projects = "Projects"
        self.realy_delete = "Realy delete"
        self.open_project = "Open project"
        self.priority = "Priority"

        self.low = "low"
        self.high = "high"

        self.short_pr = "PR"
        self.rem_days = "Remaining Days"
        self.project_part_percentage = "Percentage to the hole project"
        self.sub_task_amount = "Amount of subtasks"
        self.percent_compled = "Completed in percent"
        self.completed = "Completed"
        self.not_later_than_master = "Not later than master task"
        self.really_less_important_than_master = "Really less important tham master task?!?"
        self.description = "Description"
        self.task = "Task"
        self.app_name = "TaskAttack Project and Taskmanager"
        self.file_name = "Filename"
        self.short_description ="Short Description"

        self.project_folder = "Project Files"
        self.results_folder = "Results"
        self.auto_save_folder = "Auto save"

        self.language = "Language"
        self.days = "Days"
        self.pieces = "Pieces"

        self.no_autosave_deletion = "No auto save file deletion"
        self.autosave_deletion = "Delete auto save files to"
        self.already_exists_override = "\nalready exists!!!\nOverride?"



    def createResultFileTitle(self, kind_of_program):
        if self.not_later_than_master == "Not later than master task":
            return f"Create {kind_of_program}"
        elif self.really_less_important_than_master == "Nicht geringer als Master-Task":
            return f"{kind_of_program} erstellen"
        else:
            raise NotImplementedError("Language not completely implemented")

    @property
    def chreate_result_menu(self):
        return [self.writer, self.spreadsheet, self.presentation, self.database, self.drawing, self.gimp, self.svg]

    @property
    def menu_bar(self):
        return ([self.file, [self.new_project_sheet, self.open, self.save, self.save_at, self.exit]],
                [self.project, [self.new_project]],
                [self.edit, [self.restore_task, self.settings]],
                [self.window, [self.reload]],
                [self.help, self.about])

    @property
    def basic_button_menu(self):
        """
        fetches menu entries from chosen language for basic-button-menu-list
        :return: list of list sg.ButtonMenu.layout
        """
        return ['Unused', [self.sub_task, self.edit,
                           self.compose_results, self.chreate_result_menu,
                           self.results, [],
                           self.isolate, self.tree_view, self.delete, self.cut, self.paste, self.copy]]

    # @property
    # def b_b_m_l(self):
    #     """
    #     fetches menu entries from chosen language for basic-button-menu-list
    #     :return: list of list sg.ButtonMenu.layout
    #     """
    #     return ['Unused', [self.sub_task, self.edit,
    #                        self.compose_results, self.chreate_result_menu,
    #                        self.results, [],
    #                        self.isolate, self.delete, self.cut, self.paste, self.copy]]
    #
    # @property
    # def c_b_m_l(self):
    #     """
    #     fetches menu entries from chosen language for canged-button-menu-list
    #     :return: list of list sg.ButtonMenu.layout
    #     """
    #     return ['Unused', [self.sub_task, self.edit,
    #                        self.compose_results, self.chreate_result_menu,
    #                        self.results, [],
    #                        self.tree_view, self.delete, self.cut, self.paste, self.copy]]
    #
    @property
    def duration_types(self):
        return (self.days, self.pieces)

inter = Internationalisation("english")