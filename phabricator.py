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

        # Find the lines that are selected
        # Logic taken from https://github.com/ehamiter/ST2-GitHubinator/blob/c3fce41aaf2fc564115f83f1afef672f9a173d58/githubinator.py#L44-L49
        begin_line = view.rowcol(first_sel.begin())[0] + 1
        end_line = view.rowcol(first_sel.end())[0] + 1
        if begin_line == end_line:
            lines = begin_line
        else:
            lines = '{0}-{1}'.format(begin_line, end_line)

        # TODO: Don't forget about branches

        print lines

        # Find the file directory and name
        filepath = view.file_name()
        filedir = os.path.dirname(filepath)
        filename = os.path.basename(filepath)

        # Run `arc browse` and dump the output to the console
        browse_path = '{0}${1}'.format(filename, lines)
        popen_args = ['arc', 'browse', browse_path]
        child = subprocess.Popen(
            popen_args, cwd=filedir,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = child.stdout.read()
        stderr = child.stderr.read()
        if stdout or stderr:
            print('Ran `{0}` in `{1}`'.format(' '.join(popen_args), filedir))
            if stdout:
                print('STDOUT: {0}'.format(stdout))
            if stderr:
                print('STDERR: {0}'.format(stderr))
