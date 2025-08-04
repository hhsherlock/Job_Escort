#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Tue Jul 29 2025
    
    @author: Yaning
"""

import pandas as pd
import argparse
from datetime import date

today = date.today()
today.strftime("%Y_%m_%d")

parser = argparse.ArgumentParser()
parser.add_argument('-n','--new_file', type=str, required=True)
parser.add_argument('-o','--old_file', type=str, required=True)

args = parser.parse_args()
new_file = args.new_file
old_file = args.old_file

old_df = pd.read_csv(f'{old_file}')
new_df = pd.read_csv(f'{new_file}')

# combine the posted_time and the link to make sure they are the same
old_df['comb'] = old_df['posted_on'].astype(str) + '|' + old_df['link'].astype(str)
new_df['comb'] = new_df['posted_on'].astype(str) + '|' + new_df['link'].astype(str)

new_df['exist'] = new_df['comb'].isin(old_df['comb'])
filtered_df = new_df[~new_df['exist']]

filtered_df.to_csv(f"filtered_{today}.csv")