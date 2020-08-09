__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"


class Internationalisation:
    def __init__(self, language):
        if language == "de":
            self.setGerman()
        elif language == "en":
            self.setEnglish()

    def setGerman(self):
        # Buttons
        self.yes = "Ja"
        self.no = "Nein"
        self.start = "Start"
        self.end = "Ende"
        self.options = "Optionen"
        self.ok = "Übernehmen"
        self.cancel = "Abbrechen"

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

        self.window = "Fenster"
        self.reload = "Neu laden"
        self.help = "Hilfe"
        self.about = "Über..."

        self.sub_task = 'Unteraufgabe'
        self.compose_results = "Verfasse Resultate"
        self.results = "Results"

        self.isolate = "Isolieren"
        self.delete = "Löschen"
        self.paste = "Einfügen"
        self.cut = "Ausschneiden"
        self.copy = "Kopieren"
        self.tree_view = "Gesammtansicht"

        # texts
        self.projects = "Projekte"
        self.realy_delete = "Wirklich löschen"
        self.open_project = "Offenes Projekt"
        self.priority = "Priorität"
        self.short_pr = "PR"
        self.rem_days = "Verbleibende Tage"
        self.project_part_percentage = "Prozentualer Anteil am gesamt Projekt"
        self.sub_task_amount = "Anzahl Unteraufgaben"
        self.percent_compled = "Vollendet in Prozent"
        self.completed = "Vollendet"
        self.not_later_than_master = "Nicht später als Master-Task"
        self.not_less_important_than_master = "Nicht geringer als Master-Task"

        self.description = "Beschreibung"
        self.task = "Aufgabe"
        self.app_name = "TaskAttack Projekt und Taskmanager"
        self.file_name = "Dateiname"
        self.short_description = "Kurzbeschreibung"

    def setEnglish(self):
        # Buttons
        self.yes = "Yes"
        self.no = "No"
        self.start = "Start"
        self.end = "End"
        self.options = "Options"
        self.ok = "OK"
        self.cancel = "Cancel"

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

        self.window = "Window"
        self.reload = "Reload"
        self.help = "Help"
        self.about = "About..."

        self.sub_task = 'Subtask'
        self.compose_results = "Compose result"
        self.results = "Results"
        self.compose_results, ["writer", "spreadsheet", "gimp"], self.results, ["file1", "file2"]
        self.isolate = "Isolate"
        self.delete = "Delete"
        self.paste = "Paste"
        self.cut = "Cut"
        self.copy = "Copy"
        self.tree_view = "Tree view"

        # texts
        self.projects = "Projects"
        self.realy_delete = "Realy delete"
        self.open_project = "Open project"
        self.priority = "Priority"
        self.short_pr = "PR"
        self.rem_days = "Remaining Days"
        self.project_part_percentage = "Percentage to the hole project"
        self.sub_task_amount = "Amount of subtasks"
        self.percent_compled = "Completed in percent"
        self.completed = "Completed"
        self.not_later_than_master = "Not later than master task"
        self.not_less_important_than_master = "Not lesser than master task"
        self.description = "Description"
        self.task = "Task"
        self.app_name = "TaskAttack Project and Taskmanager"
        self.file_name = "Filename"
        self.short_description ="Short Description"


    @property
    def menu_bar(self):
        return ([self.file, [self.new_project_sheet, self.open, self.save, self.save_at, self.exit]],
                [self.project, [self.new_project]],
                [self.edit, [self.restore_task]],
                [self.window, [self.reload]],
                [self.help, self.about])

    @property
    def b_b_m_l(self):
        """
        fetches menu entries from chosen language for basic-button-menu-list
        :return: list of list sg.ButtonMenu.layout
        """
        return ['Unused', [self.sub_task, self.edit,
                           self.compose_results, ["writer", "spreadsheet", "gimp"],
                           self.results, ["file1", "file2"],
                           self.isolate, self.delete, self.cut, self.paste, self.copy]]

    @property
    def c_b_m_l(self):
        """
        fetches menu entries from chosen language for canged-button-menu-list
        :return: list of list sg.ButtonMenu.layout
        """
        return ['Unused', [self.sub_task, self.edit,
                           self.compose_results, ["writer", "spreadsheet", "gimp"],
                           self.results, ["file1", "file2"],
                           self.tree_view, self.delete, self.cut, self.paste, self.copy]]


inter = Internationalisation("en")