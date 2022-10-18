from format import init
from key2key import match, calculate_weight
from load_yml import load_file

if __name__ == '__main__':
    # 1. attack-pattern metadata
    df_ent, df_ics, df_mob, df_pre = init()

    # export
    # df_ent.to_csv('out/df_ent.csv', index=False, mode='a')
    # df_ics.to_csv('out/df_ics.csv', index=False, mode='a')
    # df_mob.to_csv('out/df_mob.csv', index=False, mode='a')
    # df_pre.to_csv('out/df_pre.csv', index=False, mode='a')

    # print(df_ics)
    # print(df_ics.loc[df_ics['attack_name'].str.contains('Compromise', case=False)])

    # 2. security rules metadata
    key = load_file("00929_Privilege_Assigned_on_Windows.yml")

    # print(key['name'])
    # print(key['remarks'])

    keywords = key['name'].split(' ') + key['remarks'].split(' ')
    # print(keyword)

    # 3、key2key map
    match_list = match(df_ics, keywords)
    rank_list = calculate_weight(match_list)

    print(rank_list)