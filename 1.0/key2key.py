def match(df, keywords):
    results = []
    for keyword in keywords:
        name_index = df.loc[df['attack_name'].str.contains(keyword, case=False)]
        description_index = df.loc[df['attack_description'].str.contains(keyword, case=False)]

        result = []
        for res in name_index.external_id:
            for tmp in res:
                result.append(tmp)
        for res in description_index.external_id:
            for tmp in res:
                result.append(tmp)
        for item in tuple(set(result)):
            results.append(item)

    return results


def calculate_weight(match_list):
    filter_list = set(match_list)

    rank_list = {}
    for item in filter_list:
        rank_list[item] = match_list.count(item)

    return sorted(rank_list.items(), key=lambda rank: rank[1], reverse=True)
