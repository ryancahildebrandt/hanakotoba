#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
Created on Sun Dec 26 11:59:10 AM EST 2021 

author: Ryan Hildebrandt 
"""

# %% Doc setup
import pandas as pd
import pickle
import re
import scipy.stats as sps

# %% pickles
with open("./data/hk_dicts.pickle", "rb") as f:
    hki_dict, hkn_dict, hk_dict = pickle.load(f)

with open("./data/meta_df.pickle", "rb") as f:
    meta_df = pickle.load(f)

with open("./data/tokenized.pickle", "rb") as f:
    tokenized = pickle.load(f)

# %% hk searching
search_names = []
for h in list(hk_dict.keys())[1:]:
    for i in hk_dict[h]["Search Names"]:
        search_names.append(i)
search_names = [i for i in search_names if not i == ""]

def hk_search(tokens_in):
    out = []
    for name in search_names:
        temp = [[e,i] for i, e in enumerate(tokens_in) if e == name]
        for t in temp:
            out.append(t)
    return out

def h_subset(h_in, results_in):
    out = []
    temp = [r for r in results_in if r[0] in hk_dict[h_in]["Search Names"]]
    for t in temp:
        out.append(t)
    return out

test = tokenized[0]
search_df = pd.DataFrame({
    "all_inc" : [hk_search(t) for t in tokenized],
    "n_tok" : [len(t) for t in tokenized]
    })

search_df["all_abs"] = [len(i) for i in search_df["all_inc"]]
search_df["all_rel"] = [i/j for i,j in zip(search_df["all_abs"], search_df["n_tok"])]
search_df["all_z"] = sps.zscore(search_df["all_rel"])

for h in list(hk_dict.keys())[1:]:
    temp = pd.DataFrame()
    temp[f'{h}_inc'] = [h_subset(h, i) for i in search_df["all_inc"]]
    temp[f'{h}_abs'] = [len(i) for i in temp[f'{h}_inc']]
    temp[f'{h}_rel'] = [i/j for i,j in zip(temp[f'{h}_abs'], search_df["n_tok"])]
    temp[f'{h}_z'] = sps.zscore(temp[f'{h}_rel'])
    search_df = pd.concat([search_df, temp], axis = 1)

azbhk_df = pd.concat([meta_df, search_df], axis = 1)
azbhk_df.to_csv("./data/azbhk_df.csv")

with open("./data/azbhk_df.pickle", 'wb') as f:
    pickle.dump(azbhk_df, f)

