#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
Created on Sun Dec 19 04:00:35 PM EST 2021 

author: Ryan Hildebrandt 
"""

# %% Doc setup
import pickle
import sudachipy

from sudachipy import dictionary
from sudachipy import tokenizer
from textwrap import wrap

# %% pickles
with open("./data/hk_dicts.pickle", "rb") as f:
    hki_dict, hkn_dict, hk_dict = pickle.load(f)

with open("./data/main_texts.pickle", "rb") as f:
    main_texts = pickle.load(f)

# %% sudachipy setup
tokenizer_obj = dictionary.Dictionary().create()
mode = tokenizer.Tokenizer.SplitMode.C

# %% tagging
def nlp_batch(in_str, nchar):
	split_text = wrap(in_str, nchar)
	morphs = [tokenizer_obj.tokenize(i, mode) for i in split_text]
	tok = []
	for morph in morphs:
		tok.append([m.normalized_form() for m in morph])
	#print(time.ctime())
	return tok[0]
	
tokenized = [nlp_batch(i, 10000) for i in main_texts]

with open("./data/tokenized.pickle", 'wb') as f:
	pickle.dump(tokenized, f)
