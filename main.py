import classification
from load_yml import load_file

if __name__ == '__main__':
    # 1. attack: classification and format
    techniques = classification.classify_by_level1('ics')
    attack_list = classification.format_by_level3(techniques)
    # print(attack_list)

    # 2. read security rules
    key = load_file("00929_Privilege_Assigned_on_Windows.yml")
    # print(key['name'])
    # print(key['remarks'])

    keywords = key['name'].split(' ') + key['remarks'].split(' ')
    print(keywords)

    # 3. key2key map
