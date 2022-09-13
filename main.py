from format import init

if __name__ == '__main__':
    df_ent, df_ics, df_mob, df_pre = init()

    print(df_ics.loc[df_ics['attack_name'].str.contains('Compromise', case=False)])
