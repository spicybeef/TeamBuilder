import json

person_dict = {}

# first = stats['first'],
# last = stats['last'],
# gender = stats['gender'],
# team = stats['team'],
# floor = stats['floor'],
# co_op = stats['co_op'],
# manager = stats['manager'],
# social_committee = stats['social_committee'],
# participating = stats['participating'],
# key = person,

with open(r'..\original_people.csv') as fp:
    # read out header
    fp.readline()
    # read out data
    for line in fp.readlines():
        line = line.replace('\r', '').replace('\n', '').split(',')
        last_name = line[0]
        first_name = line[1]
        participating = line[2]
        special = line[5]
        team = line[6]
        if team == 'O':
            team = 'Other'
        if team == 'FPGA':
            team = 'FP'
        floor = line[7]
        gender = line[8]

        key = (last_name + first_name).lower()
        person_dict[key] = {}
        person_dict[key]['first'] = first_name
        person_dict[key]['last'] = last_name
        if gender == 'F':
            person_dict[key]['gender'] = 'Female'
        else:
            person_dict[key]['gender'] = 'Male'
        person_dict[key]['team'] = team
        person_dict[key]['floor'] = floor

        if participating == 'Yes':
            person_dict[key]['participating'] = True
        else:
            person_dict[key]['participating'] = False

        person_dict[key]['current_team'] = None

        person_dict[key]['manager'] = False
        person_dict[key]['co_op'] = False
        person_dict[key]['social_committee'] = False

        if special == 'M':
            person_dict[key]['manager'] = True
        if special == 'S':
            person_dict[key]['co_op'] = True

with open(r'..\people.json', 'w') as fp:
    json.dump(person_dict, fp, sort_keys=True, separators=(',',':'), indent=4)