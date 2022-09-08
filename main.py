import pandas as pd

from stix2 import FileSystemSource
from stix2 import Filter
from stix2 import CompositeDataSource
from format import format_data

# filter
filter_objects = Filter('type', '=', 'attack-pattern')

# enterprise-attack
src_ent = FileSystemSource('./cti/enterprise-attack')
techniques_ent = src_ent.query([filter_objects])

# ics-attack
src_ics = FileSystemSource('./cti/ics-attack')
techniques_ics = src_ics.query([filter_objects])

# mobile-attack
src_mob = FileSystemSource('./cti/mobile-attack')
techniques_mob = src_mob.query([filter_objects])

# pre-attack
src_pre = FileSystemSource('./cti/pre-attack')
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

print(zip(df_pre) + zip(df_mob))
