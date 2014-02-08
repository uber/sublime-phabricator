import path
import sublime
import sublime_plugin
import subprocess


class PhabricatorOpenCommand(sublime_plugin.WindowCommand):
    def run(self):
        """Open a file inside of Phabricator with the selected lines."""
        # Get the first selection
        view = sublime.active_window().active_view()
        first_sel = view.sel()[0]

        # TODO: Find the lines that are selected
        # begin_line = 2
        lines = '2'

        print first_sel, lines

        # Find the filename
        filepath = view.file_name()
        dirname = path.os.dirname(filepath)
        filename = path.os.basename(filepath)
        # subprocess.Popen(['arc', 'browse',
