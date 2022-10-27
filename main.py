import classification
import match
from load_yml import load_file

if __name__ == '__main__':
    # 1. classification and format mitre att&ck source data
    #    column: id, type, attack_id, attack_name, attack_description
    techniques = classification.classify_by_level1('enterprise')  # ranges: pre/enterprise/mobile/ics
    attack_list = classification.format_by_level3(techniques)
    # print(attack_list)

    # 2. read security rules
    # key = load_file("./sample/" + "00927_Account_Disabled_on_Windows.yml")
    key = load_file("./sample/" + "15022_LoginLogoutAtUnusualTime.yml")
    # print(key['category'])
    # print(key['description'])
    # print(key['name'])
    # print(key['remarks'])

    # 3. match
    # strategy(a) key2key and rank
    default_list = ['category', 'name', 'remarks']  # fields of security rules
    match_list = match.key2key(attack_list, key, default_list)
    print(match.rank(match_list))
