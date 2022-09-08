import pandas as pd


def format_data(techniques):
    dict_map = {}
    for obj in techniques:
        if 'description' not in obj:
            dict_map.update({obj['id']: (obj['name'], '')})
        else:
            dict_map.update({obj['id']: (obj['name'], obj['description'])})

    pair = pd.DataFrame({'attack_id': dict_map.keys(), 'values': dict_map.values()})

    df = pd.DataFrame({'attack_id': dict_map.keys()})
    df['attack_name'] = pair['values'].apply(lambda x: x[0].encode('utf-8').strip())
    df['attack_description'] = pair['values'].apply(lambda x: x[1].encode('utf-8').strip())
    df.dropna(inplace=True)
    return df
