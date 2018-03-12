from PyQt5 import QtGui, QtCore, QtWidgets
from tb_gui_classes import *

class TeamsTabWidget(QtWidgets.QWidget):

    def __init__(self, config_sate, parent=None):
        super(TeamsTabWidget, self).__init__(parent)

        self.config_state = config_sate

        # widgets and layouts
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        # header
        self.header_widget = QtWidgets.QWidget()
        self.header_widget_layout = QtWidgets.QHBoxLayout()
        self.header_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.header_widget.setLayout(self.header_widget_layout)

        # people table view
        self.teams_tree_view = QtWidgets.QTreeView()
        self.teams_tree_view.setModel(self.config_state.team_model)
        self.teams_tree_view.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.config_state.team_model.layoutChanged.connect(self.teams_tree_view.expandAll)

        # footer
        self.footer_widget = QtWidgets.QWidget()
        self.footer_widget_layout = QtWidgets.QHBoxLayout()
        self.footer_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.footer_widget.setLayout(self.footer_widget_layout)

        self.team_number_label = QtWidgets.QLabel('Number of teams:')
        self.team_number_lineedit = QtWidgets.QLineEdit()
        self.team_number_lineedit.setFixedWidth(50)
        self.team_number_lineedit.setAlignment(QtCore.Qt.AlignHCenter)
        self.distribute_label = QtWidgets.QLabel('Distribute:')

        self.generate_button = QtWidgets.QPushButton('Generate')
        self.clear_button = QtWidgets.QPushButton('Clear')
        self.distribute_button_group = QtWidgets.QButtonGroup()
        self.distribute_random_radiobutton = QtWidgets.QRadioButton('Full Random')
        self.distribute_random_radiobutton.setChecked(True)
        self.distribute_teams_radiobutton = QtWidgets.QRadioButton('Teams')
        self.distribute_genders_radiobutton = QtWidgets.QRadioButton('Gender')
        self.distribute_button_group.addButton(self.distribute_random_radiobutton)
        self.distribute_button_group.addButton(self.distribute_teams_radiobutton)
        self.distribute_button_group.addButton(self.distribute_genders_radiobutton)
        self.footer_widget_layout.insertWidget(0, self.team_number_label)
        self.footer_widget_layout.insertWidget(1, self.team_number_lineedit)
        self.footer_widget_layout.insertWidget(2, self.distribute_label)
        self.footer_widget_layout.insertWidget(3, self.distribute_random_radiobutton)
        self.footer_widget_layout.insertWidget(4, self.distribute_teams_radiobutton)
        self.footer_widget_layout.insertWidget(5, self.distribute_genders_radiobutton)
        self.footer_widget_layout.insertStretch(6, 1)
        self.footer_widget_layout.insertWidget(7, self.clear_button)
        self.footer_widget_layout.insertWidget(8, self.generate_button)

        self.layout.addWidget(self.header_widget)
        self.layout.addWidget(self.teams_tree_view)
        self.layout.addWidget(self.footer_widget)

        self.generate_button.clicked.connect(self.generate_button_clicked)
        self.clear_button.clicked.connect(self.clear_button_clicked)

    @QtCore.pyqtSlot()
    def generate_button_clicked(self):
        # get number of teams
        lineedit_contents = self.team_number_lineedit.text()

        distribute_genders = self.distribute_genders_radiobutton.isChecked()
        distribute_teams = self.distribute_teams_radiobutton.isChecked()

        if lineedit_contents.isdigit():
            self.config_state.state['generate_teams'](int(lineedit_contents),
                                                      distribute_gender = distribute_genders,
                                                      distribute_teams = distribute_teams)
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Enter number of teams')

    @QtCore.pyqtSlot()
    def clear_button_clicked(self):
        self.config_state.state['clear_teams']()