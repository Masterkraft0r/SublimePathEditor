import os
import subprocess

import sublime, sublime_plugin

VAR = 'PATH'

class LoadPathCommand(sublime_plugin.TextCommand):
  '''Load PATH-Variable in a new view.'''
  def run(self, edit):
    current_window = self.view.window()

    if path_opened(current_window, 'PATH (SublimePathEditor)'):
      print('PATH is already opened.')
      return None

    path_view = current_window.new_file()
    path_view.set_scratch(True)
    path_view.set_name('PATH (SublimePathEditor)')
    PATH = os.environ[VAR].replace(';', '\n')
    path_view.insert(edit, 0, PATH)

class WritePathCommand(sublime_plugin.TextCommand):
  '''Write modified PATH-Variable.'''
  def run(self, edit):
    current_window = self.view.window()

    path_view = path_opened(current_window, 'PATH (SublimePathEditor)')
    if not path_view:
      print('PATH is not opened.')
      return None

    PATH = path_view.substr(sublime.Region(0, path_view.size())).replace('\n', ';')
    #subprocess.call(["start", "SublimePathEditor.bat", VAR, PATH])
    subprocess.call(['setx', '/m', VAR, PATH])
    os.environ[VAR] = PATH
    path_view.close()

def path_opened(current_window, title):
  '''Check if title'''
  views = current_window.views()
  for v in views:
    if v.name() == title:
      return v
  return None