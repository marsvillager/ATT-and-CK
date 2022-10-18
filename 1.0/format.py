import re
import pandas as pd

from stix2 import FileSystemSource
from stix2 import Filter
from stix2 import CompositeDataSource


def init():
    # filter
    filter_objects = Filter('type', '=', 'attack-pattern')

    # enterprise-attack
    src_ent = FileSystemSource('../cti/enterprise-attack')
    techniques_ent = src_ent.query([filter_objects])

    # ics-attack
    src_ics = FileSystemSource('../cti/ics-attack')
    techniques_ics = src_ics.query([filter_objects])

    # mobile-attack
    src_mob = FileSystemSource('../cti/mobile-attack')
    techniques_mob = src_mob.query([filter_objects])

    # pre-attack
    src_pre = FileSystemSource('../cti/pre-attack')
    techniques_pre = src_pre.query([filter_objects])

    # combine src
    src = CompositeDataSource()
    src.add_data_sources([src_ent, src_ics, src_mob, src_pre])

    # format
    df_ent = format_data(techniques_ent)
    df_ics = format_data(techniques_ics)
    df_mob = format_data(techniques_mob)
    df_pre = format_data(techniques_pre)

    # columns: attack_id, type, attack_name, attack_description
    df_ent.insert(1, 'type', 'ent_attack')
    df_ics.insert(1, 'type', 'ics_attack')
    df_mob.insert(1, 'type', 'mob_attack')
    df_pre.insert(1, 'type', 'pre_attack')

    # show all columns
    pd.set_option('display.max_columns', None)
    pd.set_option('expand_frame_repr', False)

    # show all columns
    # pd.set_option('display.max_rows', None)

    return df_ent, df_ics, df_mob, df_pre


def format_data(techniques):
    dict_map = {}
    for technique in techniques:
        external_id = []
        mitre_attack = technique['external_references']
        for obj in mitre_attack:
            if hasattr(obj, 'external_id'):
                external_id.append(obj.external_id)

        if 'description' not in technique:
            dict_map.update({technique['id']: (external_id, technique['name'], '')})
        else:
            dict_map.update({technique['id']: (external_id, technique['name'], technique['description'])})

    pair = pd.DataFrame({'attack_id': dict_map.keys(), 'values': dict_map.values()})

    df = pd.DataFrame({'attack_id': dict_map.keys()})
    df['external_id'] = pair['values'].apply(lambda x: x[0])
    df['attack_name'] = pair['values'].apply(lambda x: x[1])
    df['attack_description'] = pair['values'].apply(lambda x: clean_text(x[2]))
    df.dropna(inplace=True)
    return df


def replace_dots(text):
    try:
        ind = text.index('.')
        while ind < len(text) - 1:
            if not text[ind + 1:ind + 2] == ' ' and not text[ind + 1:ind + 2] == '"' and not text[
                                                                                             ind + 1:ind + 2] == '\'':
                text = text[:ind] + '_' + text[ind + 1:]
            try:
                ind = ind + 1 + text[ind + 1:].index('.')
            except:
                break
        return text
    except:
        return text


def remove_urls(text):
    text = re.sub(r'\[?\S+\]?\(?https?://\S+\)?', '', text)
    return text


def remove_citations(text):
    text = re.sub(r'\(Citations?: \S+\)', '', text)
    return text


def remove_chars(text):
    to_remove = "This technique has been deprecated. Please see ATT&CK's Initial Access and Execution tactics for " \
                "replacement techniques. "
    text = text.replace(to_remove, '')
    text = re.sub('<[^>]*>', '', text.lower()).strip()
    text = re.sub('[^a-zA-Z\'\_]', ' ', text.lower())
    return text


def clean_text(text):
    clean = remove_citations(text)
    clean = remove_urls(clean)
    clean = replace_dots(clean)
    clean = remove_chars(clean)
    return clean
