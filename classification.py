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
import stix2
from stix2 import Filter, FileSystemSource, CompositeDataSource

from format_clean import clean_text


def classify_by_level1(typeof4: str) -> list:
    """
    function: classify based on level1
    param typeof4: 4 types, pre, ent, mob, ics
    return: list of one type
    """
    # filter
    filter_objects: stix2.Filter = Filter('type', '=', 'attack-pattern')

    # xxx-attack
    src: stix2.FileSystemSource = FileSystemSource('./cti/' + typeof4 + '-attack')

    return src.query([filter_objects])


def classify_by_level2():
    """
    function: classify based on level2, pre, ent, mob, ics
    return: list of all types
    """
    # filter
    filter_objects: stix2.Filter = Filter('type', '=', 'attack-pattern')

    # all types
    src_pre: stix2.FileSystemSource = FileSystemSource('./cti/pre-attack')
    src_ent: stix2.FileSystemSource = FileSystemSource('./cti/enterprise-attack')
    src_mob: stix2.FileSystemSource = FileSystemSource('./cti/mobile-attack')
    src_ics: stix2.FileSystemSource = FileSystemSource('./cti/ics-attack')

    # combine src
    src: stix2.CompositeDataSource = CompositeDataSource()
    src.add_data_sources([src_pre, src_ent, src_mob, src_ics])

    return src.query([filter_objects])


def format_by_level3(techniques: list) -> pd.DataFrame:
    """
    function: classify and format based on level3
    param techniques: list based on level1 or level2
    return: list of properties in level3
    """
    # stage 1: preprocess
    dict_map: dict = {}
    for technique in techniques:
        # attack_id: external_id of external_references
        external_id: list = []
        mitre_attack: list = technique['external_references']
        for obj in mitre_attack:
            if hasattr(obj, 'external_id'):
                external_id.append(obj.external_id)

        # in particular cases: without x_mitre_domains or description
        if 'x_mitre_domains' and 'description' not in technique:
            dict_map.update({technique['id']: ('pre-attack', external_id, technique['name'], '')})
        elif 'description' not in technique:
            dict_map.update({technique['id']: (technique['x_mitre_domains'], external_id, technique['name'], '')})
        elif 'x_mitre_domains' not in technique:
            dict_map.update({technique['id']: ('pre-attack', external_id, technique['name'], technique['description'])})
        else:
            dict_map.update({technique['id']: (technique['x_mitre_domains'], external_id, technique['name'],
                                               technique['description'])})

    pair: pd.DataFrame = pd.DataFrame({'id': dict_map.keys(), 'values': dict_map.values()})

    # stage 2: id, type, attack_id, name, description
    df: pd.DataFrame = pd.DataFrame({'id': dict_map.keys()})
    df['type']: pd.Series = pair['values'].apply(lambda x: x[0])
    df['attack_id']: pd.Series = pair['values'].apply(lambda x: x[1])
    df['attack_name']: pd.Series = pair['values'].apply(lambda x: x[2])
    df['attack_description']: pd.Series = pair['values'].apply(lambda x: clean_text(x[3]))
    df.dropna(inplace=True)

    # show all columns
    pd.set_option('display.max_columns', None)
    pd.set_option('expand_frame_repr', False)

    # show all columns
    # pd.set_option('display.max_rows', None)

    return df
