"""
    Three different strategies have been proposed:
        -(a) key2key and rank
        -(b) rank based on dictionary of synonyms
        -(c) NLP
"""
import pandas as pd

# stop words
filer_list: list = [",", ".", "(e.g.,", "(", ")", "/", "@",
                    "a", "an", "the", "that", "this", "these", "those",
                    "on", "down", "up", "below", "in", "outside", "there", "here", "at",
                    "which", "who", "where", "why", "how", "when",
                    "or", "and", "but", "such", "so", "as", "of"]


def filter_stop_words(words: list, filer_words: list):
    """
    function: filter stop words and special characters(").")
    notes: case insensitive
    param words: origin data
    param filter_words: list of stop words
    return: data without stop words
    """
    res: list = []
    for word in words:
        flag: bool = True
        for filer_word in filer_words:
            # case insensitive
            if word.upper() == filer_word.upper():
                flag = False
                break
        if flag:
            if ")" in word:  # special case: "timeframe)."
                res.append(word[:-2])
            else:
                res.append(word)
    return res


def rank(match_list: list) -> list:
    """
    function: sort by occurrences of attack id
    param: lis of attack id
    return: order the frequencies of attack id from highest to lowest
    """
    # contestants
    filter_list: set = set(match_list)

    # frequencies
    rank_list: dict = {}
    for item in filter_list:
        rank_list[item]: int = match_list.count(item)

    return sorted(rank_list.items(), key=lambda res: res[1], reverse=True)


def key2key(attack_list: pd.DataFrame, key: dict, security_rules_list: list) -> list:
    """
    function: strategy(a) match depends on keywords
    param attack_list: range of attack source data
    param key: keywords
    param security_rules_list: range of keywords
    return: lis of attack id
    """
    keywords: list = []
    for security_rules in security_rules_list:
        keywords += key[security_rules].split(' ')

    # filter stop words
    keywords: list = filter_stop_words(keywords, filer_list)

    results: list = []
    for keyword in keywords:
        name_index: pd.DataFrame = attack_list.loc[attack_list['attack_name'].str.contains(keyword, case=False)]
        description_index: pd.DataFrame = \
            attack_list.loc[attack_list['attack_description'].str.contains(keyword, case=False)]

        result: list = []
        for res in name_index.attack_id:
            for tmp in res:
                result.append(tmp)
        for res in description_index.attack_id:
            for tmp in res:
                result.append(tmp)
        for item in tuple(set(result)):
            results.append(item)

    return results
