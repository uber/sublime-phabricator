import os
import re
try:
    # Attempt to load Python 2 quote
    from urllib import quote
except ImportError:
    # Fallback to Python 3 quote
    from urllib.parse import quote
import sublime
import sublime_plugin
import subprocess

SETTINGS_FILE = 'Phabricator.sublime-settings'


class PhabricatorOpenCommand(sublime_plugin.WindowCommand):
    def run(self):
        """Open a file inside of Phabricator with the selected lines."""
        settings = sublime.load_settings(SETTINGS_FILE)

        # Get the first selection
        view = sublime.active_window().active_view()
        first_sel = view.sel()[0]

        # Find the lines that are selected. Logic taken from:
        # https://github.com/ehamiter/ST2-GitHubinator/blob/c3fce41aaf2fc564/githubinator.py#L44-L49
        begin_line = view.rowcol(first_sel.begin())[0] + 1
        end_line = view.rowcol(first_sel.end())[0] + 1
        if begin_line == end_line:
            lines = begin_line
        else:
            lines = '{0}-{1}'.format(begin_line, end_line)

        # Find the file directory and name
        filepath = view.file_name()
        filedir = os.path.dirname(filepath)
        filename = os.path.basename(filepath)

        # Find the preselected branch
        git_branch = settings.get('branch')

        if git_branch is None and settings.get('branch_use_arc_land_onto_default', False):
            # Get current branch
            arc_args = [settings.get('arc_path', 'arc'), 'get-config', 'arc.land.onto.default']
            arc_child = subprocess.Popen(
                arc_args, cwd=filedir,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # DEV: We decode for Python 3 which receives bytes
            arc_stdout = arc_child.stdout.read().decode('utf-8')
            arc_stderr = arc_child.stderr.read().decode('utf-8')
            if arc_stderr:
                print('Ran `{0}` in `{1}`'.format(' '.join(arc_args), filedir))
                print('STDERR: {0}'.format(arc_stderr))

            # Grep the output to find the return value.
            # If something fails, git_branch will be unset and we will fallthrough into the next
            # case
            m = re.search('.*Current Value: "(?P<value>.*)"\n.*', arc_stdout)
            git_branch = m.group('value')

        # If no preselected branch is provided and we are not using arc.land.onto.default setting
        if git_branch is None:
            # Get current branch
            git_args = ['git', 'symbolic-ref', 'HEAD']
            git_child = subprocess.Popen(
                git_args, cwd=filedir,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # DEV: We decode for Python 3 which receives bytes
            git_stdout = git_child.stdout.read().decode('utf-8')
            git_stderr = git_child.stderr.read().decode('utf-8')
            if git_stderr:
                print('Ran `{0}` in `{1}`'.format(' '.join(git_args), filedir))
                print('STDERR: {0}'.format(git_stderr))

            # Strip away `refs/head` that Phabricator dislikes
            # `refs/heads/dev/my.branch` -> `dev/my.branch`
            git_branch = git_stdout.replace('refs/heads/', '').replace('\r', '').replace('\n', '')

        # Double escape branch name for Phabricator
        # `dev/my.branch` -> `dev%2Fmy.branch` -> `dev%252Fmy.branch`
        escaped_branch = quote(quote(git_branch, safe=''), safe='')

        # Run `arc browse` and dump the output to the console
        browse_path = '{0}:{1}'.format(filename, lines)
        arc_args = [
            settings.get('arc_path', 'arc'), 'browse', browse_path, '--branch', escaped_branch]
        arc_child = subprocess.Popen(
            arc_args, cwd=filedir,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        arc_stdout = arc_child.stdout.read().decode('utf-8')
        arc_stderr = arc_child.stderr.read().decode('utf-8')
        if arc_stdout or arc_stderr:
            print('Ran `{0}` in `{1}`'.format(' '.join(arc_args), filedir))
            if arc_stdout:
                print('STDOUT: {0}'.format(arc_stdout))
            if arc_stderr:
                print('STDERR: {0}'.format(arc_stderr))
