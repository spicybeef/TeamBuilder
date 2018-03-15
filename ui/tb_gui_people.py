import copy
from PyQt5 import QtGui, QtCore, QtWidgets
from tb_gui_classes import *

class AddPersonDialog(QtWidgets.QDialog):

    def __init__(self, config_state, edit_existing=False, parent=None):
        super(AddPersonDialog, self).__init__(parent)

        self.config_state = config_state

        self.edit_existing = edit_existing

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        # attributes group box
        self.attributes_groupbox = QtWidgets.QGroupBox('Attributes')
        self.attributes_groupbox_layout = QtWidgets.QGridLayout()
        self.attributes_groupbox.setLayout(self.attributes_groupbox_layout)
        self.first_name_label = QtWidgets.QLabel('First Name')
        self.first_name_lineedit = QtWidgets.QLineEdit()
        self.last_name_label = QtWidgets.QLabel('Last Name')
        self.last_name_lineedit = QtWidgets.QLineEdit()
        self.team_label = QtWidgets.QLabel('Team')
        self.team_combobox = QtWidgets.QComboBox()
        self.team_combobox.addItem('')
        self.team_combobox.addItems(self.config_state.parameters['teams'])
        self.floor_label = QtWidgets.QLabel('Floor')
        self.floor_combobox = QtWidgets.QComboBox()
        self.floor_combobox.addItem('')
        self.floor_combobox.addItems(self.config_state.parameters['floors'])
        self.gender_label = QtWidgets.QLabel('Gender')
        self.gender_button_group = QtWidgets.QButtonGroup()
        self.gender_female_radiobutton = QtWidgets.QRadioButton('Female')
        self.gender_male_radiobutton = QtWidgets.QRadioButton('Male')
        self.gender_button_group.addButton(self.gender_female_radiobutton)
        self.gender_button_group.addButton(self.gender_male_radiobutton)

        self.attributes_groupbox_layout.addWidget(self.first_name_label, 0, 0)
        self.attributes_groupbox_layout.addWidget(self.first_name_lineedit, 0, 1)
        self.attributes_groupbox_layout.addWidget(self.last_name_label, 1, 0)
        self.attributes_groupbox_layout.addWidget(self.last_name_lineedit, 1, 1)
        self.attributes_groupbox_layout.addWidget(self.team_label, 2, 0)
        self.attributes_groupbox_layout.addWidget(self.team_combobox, 2, 1)
        self.attributes_groupbox_layout.addWidget(self.floor_label, 3, 0)
        self.attributes_groupbox_layout.addWidget(self.floor_combobox, 3, 1)
        self.attributes_groupbox_layout.addWidget(self.gender_label, 4, 0)
        self.attributes_groupbox_layout.addWidget(self.gender_female_radiobutton, 4, 1)
        self.attributes_groupbox_layout.addWidget(self.gender_male_radiobutton, 5, 1)

        # special properties group box
        self.special_properties_groupbox = QtWidgets.QGroupBox('Special Properties')
        self.special_properties_groupbox_layout = QtWidgets.QGridLayout()
        self.special_properties_groupbox.setLayout(self.special_properties_groupbox_layout)
        self.participating_checkbox = QtWidgets.QCheckBox('Participating')
        self.special_properties_groupbox_layout.addWidget(self.participating_checkbox, 0, 0)
        self.student_checkbox = QtWidgets.QCheckBox('Co-op Student')
        self.special_properties_groupbox_layout.addWidget(self.student_checkbox, 1, 0)
        self.manager_checkbox = QtWidgets.QCheckBox('Manager')
        self.special_properties_groupbox_layout.addWidget(self.manager_checkbox, 2, 0)
        self.social_committee_checkbox = QtWidgets.QCheckBox('Social Commitee Member')
        self.special_properties_groupbox_layout.addWidget(self.social_committee_checkbox, 3, 0)

        # button box
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.accepted.connect(self.verify)
        self.button_box.rejected.connect(self.cancel)

        self.layout.addWidget(self.attributes_groupbox)
        self.layout.addWidget(self.special_properties_groupbox)
        self.layout.addWidget(self.button_box)

        # edit existing
        if self.edit_existing is False:
            self.setWindowTitle('Add New Person')
        else:
            self.setWindowTitle('Edit Person')
            self.first_name_lineedit.setText(self.config_state.person_placeholder.values['first'])
            self.last_name_lineedit.setText(self.config_state.person_placeholder.values['last'])
            self.gender_female_radiobutton.setChecked(self.config_state.person_placeholder.values['gender'] == 'Female')
            self.gender_male_radiobutton.setChecked(self.config_state.person_placeholder.values['gender'] == 'Male')
            self.team_combobox.setCurrentIndex(self.team_combobox.findText(self.config_state.person_placeholder.values['team']))
            self.floor_combobox.setCurrentIndex(self.floor_combobox.findText(self.config_state.person_placeholder.values['floor']))
            self.student_checkbox.setChecked(self.config_state.person_placeholder.values['co_op'])
            self.manager_checkbox.setChecked(self.config_state.person_placeholder.values['manager'])
            self.social_committee_checkbox.setChecked(self.config_state.person_placeholder.values['social_committee'])
            self.participating_checkbox.setChecked(self.config_state.person_placeholder.values['participating'])

    @QtCore.pyqtSlot()
    def verify(self):

        # check that all fields are valid
        if self.first_name_lineedit.text() == '':
            QtWidgets.QMessageBox.warning(self, 'Input Error', 'Please enter a first name')
            return
        if self.last_name_lineedit.text() == '':
            QtWidgets.QMessageBox.warning(self, 'Input Error', 'Please enter a last name')
            return
        if self.team_combobox.currentData(QtCore.Qt.DisplayRole) == '':
            QtWidgets.QMessageBox.warning(self, 'Input Error', 'Please select a team')
            return
        if self.floor_combobox.currentData(QtCore.Qt.DisplayRole) == '':
            QtWidgets.QMessageBox.warning(self, 'Input Error', 'Please select a floor')
            return
        if not self.gender_female_radiobutton.isChecked() and not self.gender_male_radiobutton.isChecked():
            QtWidgets.QMessageBox.warning(self, 'Input Error', 'Please select a gender')
            return

        if self.edit_existing is False:
            # instantiate new person
            self.config_state.person_placeholder = PersonClass()
        # otherwise the person we're editing is there already

        self.config_state.person_placeholder.values['first'] = self.first_name_lineedit.text()
        self.config_state.person_placeholder.values['last'] = self.last_name_lineedit.text()
        self.config_state.person_placeholder.values['team'] = self.team_combobox.currentData(QtCore.Qt.DisplayRole)
        self.config_state.person_placeholder.values['floor'] = self.floor_combobox.currentData(QtCore.Qt.DisplayRole)
        if self.gender_female_radiobutton.isChecked():
            self.config_state.person_placeholder.values['gender'] = 'Female'
        else:
            self.config_state.person_placeholder.values['gender'] = 'Male'
        self.config_state.person_placeholder.values['co_op'] = self.student_checkbox.isChecked()
        self.config_state.person_placeholder.values['manager'] = self.manager_checkbox.isChecked()
        self.config_state.person_placeholder.values['participating'] = self.participating_checkbox.isChecked()
        self.config_state.person_placeholder.values['social_committee'] = self.social_committee_checkbox.isChecked()
        self.config_state.person_placeholder.key = self.first_name_lineedit.text().replace(' ', '').replace('-', '') + self.last_name_lineedit.text().replace(' ', '')

        self.accept()

    @QtCore.pyqtSlot()
    def cancel(self):
        self.reject()


class PeopleTabWidget(QtWidgets.QWidget):

    def __init__(self, config_sate, parent=None):
        super(PeopleTabWidget, self).__init__(parent)

        self.config_state = config_sate

        # widgets and layouts
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        # header
        self.header_widget = QtWidgets.QWidget()
        self.header_widget_layout = QtWidgets.QHBoxLayout()
        self.header_widget.setLayout(self.header_widget_layout)
        self.header_widget_layout.setContentsMargins(0, 0, 0, 0)

        # people table view
        self.people_table_view = QtWidgets.QTableView()
        self.people_proxy_model = QtCore.QSortFilterProxyModel()
        self.people_proxy_model.setSourceModel(self.config_state.people_model)
        self.people_table_view.setModel(self.people_proxy_model)
        self.people_table_view.resizeColumnsToContents()
        self.people_table_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.people_table_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.people_table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.people_table_view.setSortingEnabled(True)
        self.people_table_view.sortByColumn(1, QtCore.Qt.AscendingOrder)

        # footer
        self.footer_widget = QtWidgets.QWidget()
        self.footer_widget_layout = QtWidgets.QHBoxLayout()
        self.footer_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.footer_widget.setLayout(self.footer_widget_layout)
        self.delete_button = QtWidgets.QPushButton('Delete')
        self.delete_button.clicked.connect(self.delete_button_clicked)
        self.edit_button = QtWidgets.QPushButton('Edit')
        self.edit_button.clicked.connect(self.edit_button_clicked)
        self.add_button = QtWidgets.QPushButton('Add')
        self.add_button.clicked.connect(self.add_button_clicked)
        self.footer_widget_layout.addWidget(self.delete_button)
        self.footer_widget_layout.addWidget(self.edit_button)
        self.footer_widget_layout.addWidget(self.add_button)
        self.footer_widget_layout.insertStretch(0, 1)

        self.layout.addWidget(self.header_widget)
        self.layout.addWidget(self.people_table_view)
        self.layout.addWidget(self.footer_widget)

    @QtCore.pyqtSlot()
    def add_button_clicked(self):
        dialog = AddPersonDialog(self.config_state, edit_existing=False)
        self.config_state.person_placeholder = PersonClass()
        self.config_state.state['add_person'](dialog)

    @QtCore.pyqtSlot()
    def edit_button_clicked(self):
        if self.people_table_view.currentIndex().isValid():
            self.config_state.person_index_placeholder = self.people_proxy_model.mapToSource(self.people_table_view.currentIndex()).row()
            self.config_state.person_placeholder = copy.copy(self.config_state.people_model.people[self.config_state.person_index_placeholder])
            dialog = AddPersonDialog(self.config_state, edit_existing=True)
            self.config_state.state['edit_person'](dialog)
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Nobody selected')

    @QtCore.pyqtSlot()
    def delete_button_clicked(self):
        if self.people_table_view.currentIndex().isValid():
            self.config_state.person_index_placeholder = self.people_proxy_model.mapToSource(self.people_table_view.currentIndex()).row()
            self.config_state.state['delete_person']()
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Nobody selected')