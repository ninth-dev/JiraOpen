import sublime, sublime_plugin
import webbrowser
import subprocess
import re

class JiraOpenIssueCommand(sublime_plugin.WindowCommand):

  def run(self):
    settings = sublime.load_settings("JiraOpen.sublime-settings")
    project_key = settings.get('projectKey')
    jira_host = settings.get('host')
    jira_issue_regex = re.compile(r'.*(' + re.escape(project_key) + r'-\d+).*')
    current_folder = self.window.extract_variables().get('folder')
    result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=current_folder, capture_output=True)
    matches = jira_issue_regex.search(result.stdout.decode('UTF-8'))

    if matches and matches.group(1):
      webbrowser.open(f"https://{jira_host}/browse/{matches.group(1)}")
    else:
      sublime.message_dialog("JiraOpen: Unable to find the issue from the git branch.")

class JiraOpenBoardCommand(sublime_plugin.WindowCommand):

  def run(self):
    settings = sublime.load_settings("JiraOpen.sublime-settings")
    if settings.get('projectKey') and settings.get('host'):
      project_key = settings.get('projectKey')
      jira_host = settings.get('host')
      webbrowser.open(f"https://{jira_host}/browse/{project_key}")
    else:
      sublime.message_dialog("JiraOpen: Unable to determine the projectKey or host from settings.")
