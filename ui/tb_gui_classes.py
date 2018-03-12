import json
import random
import datetime
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class TreeItem(object):
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            data = self.itemData[column]

            if data is None:
                return '-'
            if data is False:
                return 'No'
            if data is True:
                return 'Yes'
            else:
                return data

        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0

class TeamPlayer(TreeItem):
    def __init__(self, person, team):
        self.person = person.values
        TreeItem.__init__(self, ('',
                          self.person['first'],
                          self.person['last'],
                          self.person['gender'],
                          self.person['team'],
                          self.person['floor'],
                          self.person['co_op'],
                          self.person['manager'],
                          self.person['social_committee']), team)

class TeamModel(QtCore.QAbstractItemModel):
    def __init__(self, parent=None):
        super(TeamModel, self).__init__(parent)

        self.rootItem = TreeItem(('Team Number', 'First Name', 'Last Name', 'Gender', 'Team', 'Floor', 'Co-op', 'Manager', 'Social Committee'))

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != QtCore.Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    # list of people should have teams assigned
    def setup_model_data(self, people):

        # signal to view we are about to change
        self.layoutAboutToBeChanged.emit()

        # create a new root item
        self.rootItem = TreeItem(('Team Number', 'First Name', 'Last Name', 'Gender', 'Team', 'Floor', 'Co-op', 'Manager', 'Social Committee'))

        # keep track of teams
        teams = {}

        # keep track of non-participants
        non_participants = TreeItem(('N/A', '', '', '', '', '', '', '', ''), self.rootItem)

        # go through each person
        # keep track of teams index
        teams_index = 0
        for person in people:
            # get person's team
            team = person.values['current_team']

            # if not participating, continue
            if team is None:
                non_participants.appendChild(TeamPlayer(person, non_participants))
                continue

            # add the team if it doesn't exist
            if team not in teams:
                teams[team] = teams_index
                self.rootItem.appendChild(TreeItem((team, '', '', '', '', '', '', '', ''), self.rootItem))
                self.rootItem.childItems[-1].appendChild(TeamPlayer(person, self.rootItem.childItems[teams_index]))
                teams_index += 1
            else:
                index = teams[team]
                self.rootItem.childItems[index].appendChild(TeamPlayer(person, self.rootItem.childItems[index]))

        # sort children by team number
        self.rootItem.childItems.sort(key=lambda x: x.itemData[0])

        # add non-participants, if any
        if non_participants.childItems:
            self.rootItem.appendChild(non_participants)

        # update team counts
        self.update_team_counts()

        # end model change
        self.layoutChanged.emit()

    def update_team_counts(self):

        for team in self.rootItem.childItems:
            team.itemData = (str(team.itemData[0]) + ' (%i)' % len(team.childItems), '', '', '', '', '', '', '', '')

# people model, holds people
class PeopleModel(QtCore.QAbstractTableModel):

    def __init__(self, parent=None):
        super(PeopleModel, self).__init__(parent)

        self.people = []
        self.headers = ['Team Number', 'First Name', 'Last Name', 'Gender', 'Team', 'Floor', 'Co-op', 'Manager', 'Social Committee', 'Participating']
        self.key_to_header_index = ['current_team', 'first', 'last', 'gender', 'team', 'floor', 'co_op', 'manager', 'social_committee', 'participating']

    # return the total amount of rows
    def rowCount(self, parent=None):
        return len(self.people)

    # return the total amount of columns
    def columnCount(self, parent=None):
        return len(self.headers)

    # return header data for given column
    def headerData(self, index, orientation, role=None):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.headers[index]

    # return the data at a given index
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            data = self.people[index.row()].values[self.key_to_header_index[index.column()]]
            if data is None:
                return '-'
            if data is False:
                return 'No'
            if data is True:
                return 'Yes'
            else:
                return data

    # appends a new person at index
    def insert_person(self, index, person):
        self.layoutAboutToBeChanged.emit()
        self.people.insert(index, person)
        self.layoutChanged.emit()

    # remove person at index
    def remove_person(self, index):
        self.layoutAboutToBeChanged.emit()
        del self.people[index]
        self.layoutChanged.emit()

    # clear people
    def clear_people(self):
        self.layoutAboutToBeChanged.emit()
        self.people = []
        self.layoutChanged.emit()

    # assign team to index
    def assign_team(self, index, team):
        self.layoutAboutToBeChanged.emit()
        self.people[index].values['current_team'] = team
        self.layoutChanged.emit()

    # clear team of index
    def clear_team(self, index):
        self.layoutAboutToBeChanged.emit()
        self.people[index].values['current_team'] = None
        self.layoutChanged.emit()

# class defining a person
class PersonClass:

    def __init__(self, first=None, last=None, gender=None, team=None, floor=None, participating=False, co_op=False, manager=False, social_committee=False, current_team=None, key=None, parent=None):

        self.values = {}
        self.values['first'] = first
        self.values['last'] = last
        self.values['gender'] = gender
        self.values['team'] = team
        self.values['floor'] = floor
        self.values['co_op'] = co_op
        self.values['manager'] = manager
        self.values['social_committee'] = social_committee
        self.values['current_team'] = current_team
        self.values['participating'] = participating
        self.key = key

    def keys(self):
        return self.values.keys()

# configuration state class
class ConfigState(QtCore.QObject):

    def __init__(self, parent=None):
        super(ConfigState, self).__init__(parent)

        # models
        self.people_model = PeopleModel()
        self.team_model = TeamModel()

        # parameters
        self.parameters = {}

        # dict of functions
        self.state = {
            'default': self.state_default,
            'add_person': self.state_add_person,
            'edit_person': self.state_edit_person,
            'delete_person': self.state_delete_person,
            'load_people': self.state_load_people,
            'save_people_json': self.state_save_people_json,
            'save_people_csv': self.state_save_people_csv,
            'generate_teams': self.state_generate_teams,
            'clear_teams': self.state_clear_teams,
        }

        # person placeholder
        self.person_placeholder = None
        # person index placeholder
        self.person_index_placeholder = None

    # get current script path
    def get_script_path(self):
        return os.path.dirname(os.path.realpath(sys.argv[0]))

    # cycle idle state
    def state_default(self):
        pass

    # delete person state
    def state_delete_person(self):
        self.people_model.remove_person(self.person_index_placeholder)

    # add person state
    def state_add_person(self, dialog):
        if dialog.exec_():
            # insert the person at the end of the list
            self.people_model.insert_person(len(self.people_model.people), self.person_placeholder)

    # edit person state
    def state_edit_person(self, dialog):
        if dialog.exec_():
            # accepted
            # remove old entry
            self.people_model.remove_person(self.person_index_placeholder)
            # add new entry
            self.people_model.insert_person(self.person_index_placeholder, self.person_placeholder)
        else:
            # rejected
            # do nothing
            pass

    # load some people
    def state_load_people(self):

        # get a file name
        path = os.path.join(self.get_script_path(), '..')
        load_dialog_result = QtWidgets.QFileDialog.getOpenFileName(self.parent(), 'Load Some People' , path, filter='*.json')
        file_name = load_dialog_result[0]

        # if we have a valid file name, load the file
        if file_name is not '':
            with open(file_name, 'r') as fp:
                new_people = json.load(fp)
        else:
            return

        # clear people
        self.people_model.clear_people()

        # add people if all keys present
        for person, stats in new_people.items():
            if all (key in stats for key in ('current_team', 'first', 'last', 'gender', 'team', 'floor', 'co_op', 'manager', 'social_committee', 'participating')):
                new_person = PersonClass(
                    first = stats['first'],
                    last = stats['last'],
                    gender = stats['gender'],
                    team = stats['team'],
                    floor = stats['floor'],
                    co_op = stats['co_op'],
                    manager = stats['manager'],
                    social_committee = stats['social_committee'],
                    participating = stats['participating'],
                    key = person,
                )

                self.people_model.insert_person(len(self.people_model.people), new_person)

    # save some people JSON
    def state_save_people_json(self):

        # gather all the people
        out_dict = {}
        for person in self.people_model.people:
            out_dict[person.key] = person.values

        # get a file name
        path = os.path.join(self.get_script_path(), '..')
        save_dialog_result = QtWidgets.QFileDialog.getSaveFileName(self.parent(), 'Save Some People' , path, filter='*.json')
        file_name = save_dialog_result[0]

        # if we have a valid file name, load the file
        if file_name is not '':
            with open(file_name, 'w') as fp:
                json.dump(out_dict, fp, sort_keys=True, separators=(',',':'), indent=4)

    # save some people CSV
    def state_save_people_csv(self):

        # get a file name
        path = os.path.join(self.get_script_path(), '..')
        save_dialog_result = QtWidgets.QFileDialog.getSaveFileName(self.parent(), 'Save Some People' , path, filter='*.csv')
        file_name = save_dialog_result[0]

        if file_name is not '':
            try:
                with open(file_name, 'w') as fp:
                    # write headers
                    for header in PeopleModel().headers:
                        fp.write(header + ',')
                    # new line
                    fp.write(str('\n'))
                    # write data
                    for person in self.people_model.people:
                        for key in PeopleModel().key_to_header_index:
                            fp.write(str(person.values[key]) + ',')
                        # new line
                        fp.write(str('\n'))
            except:
                QtWidgets.QMessageBox.critical(self.parent(), 'File Error', 'Couldn\'t write to file!')

    # generate some teams
    def state_generate_teams(self, num_teams, distribute_teams=False, distribute_gender=False):

        # assign a team completely randomly
        if not distribute_gender and not distribute_teams:
            # keep track of those no longer in the pool
            picked = []
            # and those currently in the pool
            pool = []
            # clear current teams and add indices to trackers
            for index in range(len(self.people_model.people)):
                self.people_model.clear_team(index)
                if self.people_model.people[index].values['participating']:
                    pool.append(index)
                else:
                    picked.append(index)

            # while we have people in the pool, give them a team
            team_index = 1
            while pool:
                # seed the randomizer
                random.seed(datetime.datetime.now())
                # get a random position
                random_index = random.randint(0, len(pool)-1)
                # put that person on a team
                self.people_model.assign_team(pool.pop(random_index), team_index)
                # go to the next team
                team_index += 1
                # wrap around
                if team_index == num_teams + 1:
                    team_index = 1

        # distribute genders across teams
        if distribute_gender:
            # keep track of those no longer in the pool
            picked = []
            # women that are participating
            women_pool = []
            # men that are participating
            men_pool = []
            # clear current teams and add indices to trackers
            for index in range(len(self.people_model.people)):
                self.people_model.clear_team(index)
                if self.people_model.people[index].values['participating']:
                    if self.people_model.people[index].values['gender'] == 'Female':
                        women_pool.append(index)
                    else:
                        men_pool.append(index)
                else:
                    picked.append(index)

            # while we have people in the women pool, give them a team
            team_index = 1
            while women_pool:
                # seed the randomizer
                random.seed(datetime.datetime.now())
                # get a random position
                random_index = random.randint(0, len(women_pool)-1)
                # put that person on a team
                self.people_model.assign_team(women_pool.pop(random_index), team_index)
                # go to the next team
                team_index += 1
                # wrap around
                if team_index == num_teams + 1:
                    team_index = 1

            # while we have people in the men pool, give them a team
            while men_pool:
                # seed the randomizer
                random.seed(datetime.datetime.now())
                # get a random position
                random_index = random.randint(0, len(men_pool)-1)
                # put that person on a team
                self.people_model.assign_team(men_pool.pop(random_index), team_index)
                # go to the next team
                team_index += 1
                # wrap around
                if team_index == num_teams + 1:
                    team_index = 1

        # distribute teams across teams
        if distribute_teams:
            # keep track of those no longer in the pool
            picked = []
            # set up pools for each team
            pools = {}
            for team in self.parameters['teams']:
                pools[team] = []
            # clear current teams and add indices to trackers
            for index in range(len(self.people_model.people)):
                self.people_model.clear_team(index)
                if self.people_model.people[index].values['participating']:
                    team = self.people_model.people[index].values['team']
                    pools[team].append(index)
                else:
                    picked.append(index)
            # iterate through each team
            team_index = 1
            for team in self.parameters['teams']:
                while pools[team]:
                    # seed the randomizer
                    random.seed(datetime.datetime.now())
                    # get a random position
                    random_index = random.randint(0, len(pools[team])-1)
                    # put that person on a team
                    self.people_model.assign_team(pools[team].pop(random_index), team_index)
                    # go to the next team
                    team_index += 1
                    # wrap around
                    if team_index == num_teams + 1:
                        team_index = 1

        # populate the team model from the people
        self.team_model.setup_model_data(self.people_model.people)

    # save some people JSON
    def state_clear_teams(self):

        # clear current teams and add indices to trackers
        for index in range(len(self.people_model.people)):
            self.people_model.clear_team(index)
        # populate the team model from the people
        self.team_model.setup_model_data(self.people_model.people)