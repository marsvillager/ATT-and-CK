from load_yml import load_file
from tools.relationshiphelpers import get_srcs, mitigation_mitigates_techniques

if __name__ == '__main__':
    # 1. classification and format mitre att&ck source data
    #    column: id, type, attack_id, attack_name, attack_description
    # techniques: list = attack_classification.classify_by_level1('enterprise')  # ranges: pre/enterprise/mobile/ics
    # attack_dict: dict = attack_classification.format_by_level3(techniques)
    # print(attack_dict)

    update = False
    # print("Update data or not?Please input yes or no")
    # if input() == 'yes':
    #     update = True

    mitigation_dict: dict = mitigation_mitigates_techniques(get_srcs(update))
    for mitigation in mitigation_dict:
        print(mitigation)
        mitigation_list = mitigation_dict[mitigation]
        for item in mitigation_list:
            attack_object: dict = item['object']
            print(attack_object['external_references'][0]['external_id'])

            relationship: dict = item['relationship']
            print(relationship)




    # 2. read security rules
    # key: dict = load_file("./security_rules/" + "00927_Account_Disabled_on_Windows.yml")
    # key: dict = load_file("./security_rules/" + "00928_Account_Enabled_on_Windows.yml")
    key: dict = load_file("./security_rules/" + "15022_LoginLogoutAtUnusualTime.yml")
    # print(key['category'])
    # print(key['description'])
    # print(key['name'])
    # print(key['remarks'])

    # 3. match
    # strategy(a) key2key and rank
    # default_list: list[str] = ['category', 'name', 'remarks']  # fields of security rules
    # match_list: list = match.key2key(attack_list, key, default_list)
    # print(match.rank(match_list))
