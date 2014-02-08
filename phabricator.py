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

        # Find the file directory and name
        filepath = view.file_name()
        filedir = os.path.dirname(filepath)
        filename = os.path.basename(filepath)

        # Run `arc browse` and dump the output to the console
        child = subprocess.Popen(
            ['arc', 'browse', filename], cwd=filedir,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = child.stdout.read()
        stderr = child.stderr.read()
        if stdout or stderr:
            print('Ran `arc browse {0}`'.format(filename))
            if stdout:
                print('STDOUT: {0}'.format(stdout))
            if stderr:
                print('STDERR: {0}'.format(stderr))
