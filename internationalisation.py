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
        self.browse = "Browse"
        self.cancel = "Abbrechen"
        self.end = "Ende"
        self.no = "Nein"
        self.ok = "Übernehmen"
        self.options = "Optionen"
        self.own_folder_setup = "Eigene Ordner Strucktur"
        self.standard_folder_setup = "Standard Ordner"
        self.start = "Start"
        self.yes = "Ja"

        # Menu entries
        self.about = "Über..."
        self.add_link = "Web-Link hinzufügen"
        self.compose_results = "Verfasse Ergebnisse"
        self.copy = "Kopieren"
        self.cut = "Ausschneiden"
        self.database = "Datenbank"
        self.delete = "Löschen"
        self.drawing = "Office-Zeichnung"
        self.edit = "Bearbeiten"
        self.exit = "Beenden"
        self.file = "Datei"
        self.gimp = "Pixel-Grafik"
        self.help = "Hilfe"
        self.isolate = "Isolieren"
        self.new_project = "Neues Projekt"
        self.new_project_sheet = "Neue Projekt Tabelle"
        self.open = "Öffnen"
        self.paste = "Einfügen"
        self.presentation = "Präsentation"
        self.project = "Projekt"
        self.reload = "Neu laden"
        self.restore_task = "Aufgabe widerherstellen"
        self.results = "Ergebnisse"
        self.save = "Speichern"
        self.save_at = "Speichern in"
        self.settings = "Einstellungen"
        self.spreadsheet = "Tabellenkalkulation"
        self.sub_task = 'Unteraufgabe'
        self.svg = "Vektor-Grafik"
        self.tree_view = "Gesammtansicht"
        self.window = "Fenster"
        self.writer = "Text"

        # texts
        self.already_exists_override = "\nbesteht bereits!!!\nÜberschreiben?"
        self.app_name = "TaskAttack Projekt und Taskmanager"
        self.auto_save_folder =  "Autospeichern"
        self.autosave_deletion = "Autospeicherdateien löschen bis auf"
        self.completed = "Vollendet"
        self.days = "Tage"
        self.description = "Beschreibung"
        self.enter_weblink = "Weblink eingeben"
        self.file_name = "Dateiname"
        self.high = "high"
        self.language = "Sprache"
        self.low = "low"
        self.no_autosave_deletion = "Kein Löschen der Autospeicherdateien"
        self.not_later_than_master = "Nicht später als Master-Task"
        self.open_project = "Offenes Projekt"
        self.percent_compled = "Vollendet in Prozent"
        self.pieces = "Stück"
        self.priority = "Priorität"
        self.project_folder = "Projekt Ordner"
        self.project_part_percentage = "Prozentualer Anteil am gesamt Projekt"
        self.projects = "Projekte"
        self.really_less_important_than_master = "Wirklich unwichtiger als Master-Task?!?"
        self.realy_delete = "Wirklich löschen"
        self.rem_days = "Verbleibende Tage"
        self.results_folder = "Ergebnisse"
        self.short_description = "Kurzbeschreibung"
        self.short_pr = "PR"
        self.sub_task_amount = "Anzahl Unteraufgaben"
        self.task = "Aufgabe"
        self.web_link = "Web-Link"
        self.web_links = "Web-Links"

    def _setEnglish(self):
        # Buttons
        self.browse = "Browse"
        self.cancel = "Cancel"
        self.end = "End"
        self.no = "No"
        self.ok = "OK"
        self.options = "Options"
        self.own_folder_setup = "Own folder setup"
        self.standard_folder_setup = "Standard folders"
        self.start = "Start"
        self.yes = "Yes"

        # Menu entries
        self.about = "About..."
        self.add_link = "Add Web-Link"
        self.compose_results = "Compose result"
        self.copy = "Copy"
        self.cut = "Cut"
        self.database = "Database"
        self.delete = "Delete"
        self.drawing = "Drawing"
        self.edit = "Edit"
        self.exit = "Exit"
        self.file = "File"
        self.gimp = "Pixel-Manipulation"
        self.help = "Help"
        self.isolate = "Isolate"
        self.new_project = "New Project"
        self.new_project_sheet = "New Project Sheet"
        self.open = "Open"
        self.paste = "Paste"
        self.presentation = "Presentation"
        self.project = "Project"
        self.reload = "Reload"
        self.restore_task = "Restore Task"
        self.results = "Results"
        self.save = "Save"
        self.save_at = "Save at"
        self.settings = "Settings"
        self.spreadsheet = "Spreadsheet"
        self.sub_task = 'Subtask'
        self.svg = "Vektor-Manipulation"
        self.tree_view = "Tree view"
        self.window = "Window"
        self.writer = "Writer"

        # texts
        self.already_exists_override = "\nalready exists!!!\nOverride?"
        self.app_name = "TaskAttack Project and Taskmanager"
        self.auto_save_folder = "Auto save"
        self.autosave_deletion = "Delete auto save files to"
        self.completed = "Completed"
        self.days = "Days"
        self.description = "Description"
        self.enter_weblink = "Enter Weblink"
        self.file_name = "Filename"
        self.high = "high"
        self.language = "Language"
        self.low = "low"
        self.no_autosave_deletion = "No auto save file deletion"
        self.not_later_than_master = "Not later than master task"
        self.open_project = "Open project"
        self.percent_compled = "Completed in percent"
        self.pieces = "Pieces"
        self.priority = "Priority"
        self.project_folder = "Project Files"
        self.project_part_percentage = "Percentage to the hole project"
        self.projects = "Projects"
        self.really_less_important_than_master = "Really less important tham master task?!?"
        self.realy_delete = "Realy delete"
        self.rem_days = "Remaining Days"
        self.results_folder = "Results"
        self.short_description ="Short Description"
        self.short_pr = "PR"
        self.sub_task_amount = "Amount of subtasks"
        self.task = "Task"
        self.web_link = "Web-Link"
        self.web_links = "Web-Links"

    def createResultFileTitle(self, kind_of_program):
        if self.not_later_than_master == "Not later than master task":
            return f"Create {kind_of_program}"
        elif self.really_less_important_than_master == "Nicht geringer als Master-Task":
            return f"{kind_of_program} erstellen"
        else:
            raise NotImplementedError("Language not completely implemented")

    @property
    def result_programms_list(self):
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
                           self.compose_results, self.result_programms_list,
                           self.results, [],
                           self.add_link, self.web_links, [],
                           self.isolate, self.tree_view, self.delete, self.cut, self.paste, self.copy]]
    @property
    def duration_types(self):
        return (self.days, self.pieces)

inter = Internationalisation("english")