import sys
import os
import time
import datetime
import json
from PyQt5 import QtGui, QtCore, QtWidgets
from tb_gui_classes import *
from tb_gui_people import *
from tb_gui_teams import *

# Current date
def current_date(only_date=False):
    ts = time.time()
    if only_date:
        return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
    else:
        return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

class WorkflowTabWidget(QtWidgets.QTabWidget):

    def __init__(self, config_state, parent=None):
        super(WorkflowTabWidget, self).__init__(parent)

        self.config_state = config_state

        people_tab_widget = PeopleTabWidget(config_state)
        teams_tab_widget = TeamsTabWidget(config_state)

        self.addTab(people_tab_widget, "People")
        self.addTab(teams_tab_widget, "Teams")

# main container widget
# switches between the different views
class MainContainerWidget(QtWidgets.QWidget):

    def __init__(self, config_state, parent=None):
        super(MainContainerWidget, self).__init__(parent)
        # program state machine
        self.config_state = config_state

        # instantiate all program widgets
        self.workflow_tab_view = WorkflowTabWidget(config_state)

        # append items to views, initially disabled
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.workflow_tab_view,0,0)

# main window
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, config_state, parent=None):
        super(MainWindow, self).__init__(parent)

        self.config_state = config_state

        #menu bar
        self.menu_bar = MenuBar(config_state)

        #status bar
        self.status_bar = StatusBar(config_state)

        #main window items
        self.main_container_widget = MainContainerWidget(config_state)

        #main window attributes
        self.setWindowTitle(self.config_state.parameters["app_name"])
        self.setMenuBar(self.menu_bar)
        self.setStatusBar(self.status_bar)
        self.setCentralWidget(self.main_container_widget)
        self.setMinimumHeight(600)
        self.setMinimumWidth(1000)

        #signal connections

# menu bar
class MenuBar(QtWidgets.QMenuBar):

    def __init__(self, config_state, parent=None):
        super(MenuBar, self).__init__(parent)

        self.config_state = config_state


        #menu items
        self.file_menu = self.addMenu("&File")
        self.help_menu = self.addMenu("&Help")

        #file menu actions

        self.load_people_action = QtWidgets.QAction(QtGui.QIcon('load.png'), '&Load People', self)
        self.load_people_action.setShortcut('Ctrl+O')
        self.load_people_action.setStatusTip('Load some people')
        self.load_people_action.triggered.connect(self.config_state.state['load_people'])

        self.save_people_json_action = QtWidgets.QAction(QtGui.QIcon('save.png'), '&Save People (JSON)', self)
        self.save_people_json_action.setShortcut('Ctrl+S')
        self.save_people_json_action.setStatusTip('Save the people (JSON)')
        self.save_people_json_action.triggered.connect(self.config_state.state['save_people_json'])

        self.save_people_csv_action = QtWidgets.QAction(QtGui.QIcon('save.png'), '&Save People (CSV)', self)
        self.save_people_csv_action.setShortcut('Shift+Ctrl+S')
        self.save_people_csv_action.setStatusTip('Save the people (CSV)')
        self.save_people_csv_action.triggered.connect(self.config_state.state['save_people_csv'])

        self.quit_program_action = QtWidgets.QAction(QtGui.QIcon("exit.png"), "&Quit", self)
        self.quit_program_action.setShortcut("Ctrl+Q")
        self.quit_program_action.setStatusTip("Quit the program")
        self.quit_program_action.triggered.connect(QtWidgets.qApp.quit)

        #help menu actions
        self.documentation_action = QtWidgets.QAction("Documentation...", self)
        self.documentation_action.setStatusTip("How do you even use this thing?")
        self.about_action = QtWidgets.QAction("About...", self)
        self.about_action.setStatusTip("Who are the amazing people behind this program?")

        #file menu config
        self.file_menu.addAction(self.load_people_action)
        self.file_menu.addAction(self.save_people_json_action)
        self.file_menu.addAction(self.save_people_csv_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.quit_program_action)
        #help menu config
        self.help_menu.addAction(self.documentation_action)
        self.help_menu.addSeparator()
        self.help_menu.addAction(self.about_action)

class StatusBar(QtWidgets.QStatusBar):

    def __init__(self, config_state, parent = None):
        super(StatusBar, self).__init__(parent)

        self.config_state = config_state

        self.setContentsMargins(0, 0, 0, 0)

        self.program_version_label = QtWidgets.QLabel()
        self.current_date_label = QtWidgets.QLabel()

        self.program_version_label.setText("Version: " + config_state.parameters["version"])
        self.current_date_label.setText("Date: " + current_date(only_date = True))

        self.addWidget(self.program_version_label)
        self.addWidget(self.current_date_label)

        self.setFixedHeight(30)

def main():

    # initialize config state
    config_state = ConfigState()
    config_state.state["default"]()

    # get script path
    path = config_state.get_script_path()

    # load parameters
    with open(os.path.join(path, 'tb_gui_params.json'), 'r') as fp:
        config_state.parameters = json.load(fp)

    global app
    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow(config_state)
    config_state.setParent(form)
    form.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()