"""
    classification framework:
        -level1:
            -- pre-attack
            -- enterprise-attack
            -- mobile-attack
            -- ics-attack

        -level2:
            -- attack_pattern

        -level3:
            -- id(primary key: attack-pattern id)
            -- name
            -- description
            -- external_id in external_references(mitre att&ck id, capec id and so on)
            -- x_mitre_domains

    techniques: stix2

    format: pandas.DataFrame
"""
import pandas as pd
from stix2 import Filter, FileSystemSource, CompositeDataSource

from format_clean import clean_text


def classify_by_level1(typeof4):
    # filter
    filter_objects = Filter('type', '=', 'attack-pattern')

    # xxx-attack
    src = FileSystemSource('./cti/' + typeof4 + '-attack')
    return src.query([filter_objects])


def classify_by_level2():
    # filter
    filter_objects = Filter('type', '=', 'attack-pattern')

    # all types
    src_pre = FileSystemSource('./cti/pre-attack')
    src_ent = FileSystemSource('./cti/enterprise-attack')
    src_mob = FileSystemSource('./cti/mobile-attack')
    src_ics = FileSystemSource('./cti/ics-attack')

    # combine src
    src = CompositeDataSource()
    src.add_data_sources([src_pre, src_ent, src_mob, src_ics])

    return src.query([filter_objects])


# level3: id, type, attack_id, name, description
def format_by_level3(techniques):
    dict_map = {}
    for technique in techniques:
        # attack_id: external_id of external_references
        external_id = []
        mitre_attack = technique['external_references']
        for obj in mitre_attack:
            if hasattr(obj, 'external_id'):
                external_id.append(obj.external_id)

        # in particular cases: without x_mitre_domains or description
        if 'x_mitre_domains' and 'description' not in technique:
            dict_map.update(
                {technique['id']: ('pre-attack', external_id, technique['name'], '')})
        elif 'description' not in technique:
            dict_map.update({technique['id']: (
                technique['x_mitre_domains'], external_id, technique['name'], '')})
        elif 'x_mitre_domains' not in technique:
            dict_map.update({technique['id']: (
                'pre-attack', external_id, technique['name'], technique['description'])})
        else:
            dict_map.update(
                {
                    technique['id']: (
                        technique['x_mitre_domains'],
                        external_id,
                        technique['name'],
                        technique['description'])})

    pair = pd.DataFrame({'id': dict_map.keys(), 'values': dict_map.values()})

    df = pd.DataFrame({'id': dict_map.keys()})
    df['type'] = pair['values'].apply(lambda x: x[0])
    df['attack_id'] = pair['values'].apply(lambda x: x[1])
    df['attack_name'] = pair['values'].apply(lambda x: x[2])
    df['attack_description'] = pair['values'].apply(lambda x: clean_text(x[3]))
    df.dropna(inplace=True)

    # show all columns
    pd.set_option('display.max_columns', None)
    pd.set_option('expand_frame_repr', False)

    # show all columns
    # pd.set_option('display.max_rows', None)

    return df
