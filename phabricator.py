import os
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

        # TODO: Don't forget about branches

        print first_sel, lines

        # Find the filename
        filepath = view.file_name()
        filedir = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        print filedir, filename
        print filename
        print os.environ['PATH']
        # child = subprocess.Popen(
        #     'ruby browse {0}'.format(filename), shell=True, cwd=filedir,
        #     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # print child.stdout.read()
        # print child.stderr.read()
