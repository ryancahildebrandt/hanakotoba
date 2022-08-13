#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
Created on Tue Mar  1 10:13:51 AM EST 2022 

author: Ryan Hildebrandt 
"""

# Doc setup
#import datetime as dt
import dateutil as du
import itertools as it
import numpy as np
import pandas as pd
import pickle
import re

from astropy.time import Time

# pickles
with open("./data/azbhk_df.pickle", "rb") as f:
	azbhk_df = pickle.load(f)

with open("./data/hk_dicts.pickle", "rb") as f:
	hki_dict, hkn_dict, hk_dict = pickle.load(f)

# genres from wikipedia
genres = pd.read_csv("./data/分類番号.csv")
genre_dict = {i:g for i,g in genres.values}
azbhk_df["category_number"] = [int(i.strip("[NDCK ]")[:3]) if isinstance(i, str) else "" for i in azbhk_df["category_number"]]
azbhk_df["category_number"] = azbhk_df["category_number"].map(genre_dict)
genres.to_csv("./outputs/genres.csv")

azbhk_df["author"] = [f"{i}{j}" for i,j in zip(azbhk_df["last_name"],azbhk_df["first_name"])]

#date things
#eras https://kids.kiddle.co/List_of_Japanese_eras and wikipedia
#pandas datetime throws out of bound datetime for early authors, using astropy
jidai = pd.read_csv("./data/時代.csv")
jidai["終"] = [i-1 for i in jidai.iloc[1:,0].tolist() + [2023]]
jidai_dict = {j:{"start" : i, "end" : k} for i,j,k in jidai.values}
jidai.to_csv("./outputs/jidai.csv")

gannen = pd.read_csv("./data/元年.csv")
gannen["終"] = [i-1 for i in gannen.iloc[1:,0].tolist() + [2023]]
gannen_dict = {j:{"start" : i, "end" : k} for i,j,k in gannen.values}
gannen.to_csv("./outputs/gannen.csv")

def date_clean(in_date):
	if not isinstance(in_date, str):
		out = ""
	elif in_date in ["紀元前7世紀末", "紀元前6世紀初", "不詳", ""]:
		out = {
		"紀元前7世紀末" : Time(-630, format='jyear').ymdhms,
		"紀元前6世紀初" : Time(-570, format='jyear').ymdhms,
		"不詳" : "",
		"" : ""
		}[in_date]
	else:
		in_date = re.sub("--|年|日|月","-", in_date)
		in_date = re.sub(" |(（|\().*(）|\))|(～|,).*||[改版発行初刷第復刻訂新号再増補]|\u3000", "", in_date)
		in_date = re.sub("([\d]{4})(\d)","\g<1>-\g<2>", in_date)
		if re.search("\d{1,4}-?\d{1,2}?-?\d{1,2}?", in_date):
			in_date = re.search("\d{1,4}-?\d{1,2}?-?\d{1,2}?", in_date).group()
			out = Time(du.parser.parse(in_date)).ymdhms
		else:
			out = ""
		#if len(in_date) == 4:
		#	in_date = in_date + "-01-01"
	return out

def get_jidai(y):
	inds = [jidai_dict[i]["start"] < y <  jidai_dict[i]["end"] for i in jidai_dict.keys()]
	out = list(it.compress(jidai_dict.keys(), inds))
	if len(out) == 0:
		out = ""
	else:
		out = out[0]
	return out

def get_gannen(y):
	inds = [gannen_dict[i]["start"] < y <  gannen_dict[i]["end"] for i in gannen_dict.keys()]
	out = list(it.compress(gannen_dict.keys(), inds))
	if len(out) == 0:
		out = ""
	else:
		out = out[0]
	return out

azbhk_df["first_pub_date"] = [date_clean(i) for i in azbhk_df["original_first_edition_publication_year_1"]]
azbhk_df["date_of_birth"] = [date_clean(i) for i in azbhk_df["date_of_birth"]]
azbhk_df["date_of_death"] = [date_clean(i) for i in azbhk_df["date_of_death"]]

azbhk_df["pub_year"] = [i if i == "" else i["year"] for i in azbhk_df["first_pub_date"]]
azbhk_df["pub_decade"] = [i if i == "" else (i["year"]//10)*10 for i in azbhk_df["first_pub_date"]]
azbhk_df["pub_century"] = [i if i == "" else (i["year"]//100)*100 for i in azbhk_df["first_pub_date"]]
azbhk_df["pub_jidai"] = ["" if i == "" else get_jidai(i) for i in azbhk_df["pub_year"]]
azbhk_df["pub_gannen"] = ["" if i == "" else get_gannen(i) for i in azbhk_df["pub_year"]]
azbhk_df["pub_month"] = [i if i == "" else i["month"] for i in azbhk_df["first_pub_date"]]

azbhk_df["birth_year"] = [i if i == "" else i["year"] for i in azbhk_df["date_of_birth"]]
azbhk_df["birth_decade"] = [i if i == "" else (i["year"]//10)*10 for i in azbhk_df["date_of_birth"]]
azbhk_df["birth_century"] = [i if i == "" else (i["year"]//100)*100 for i in azbhk_df["date_of_birth"]]
azbhk_df["birth_jidai"] = ["" if i == "" else get_jidai(i) for i in azbhk_df["birth_year"]]
azbhk_df["birth_gannen"] = ["" if i == "" else get_gannen(i) for i in azbhk_df["birth_year"]]
azbhk_df["birth_month"] = [i if i == "" else i["month"] for i in azbhk_df["date_of_birth"]]

# separate empty cols
azbhk_full_df = azbhk_df.copy()

azbhk_df = azbhk_df.replace(0, np.nan).dropna(axis = 1, how =  "all")
azbhk_df = azbhk_df.drop([n for n in azbhk_df.columns if re.search("_inc", n) and sum([len(i) for i in azbhk_df[n]]) == 0], axis = 1)
azbhk_e_list = [i for i in azbhk_df.columns if i not in azbhk_full_df.columns]

meta_cols = list(azbhk_df.columns[:58])
base_cols = ["work_id", "work_name", "subtitle", "category_number", "first_name", "last_name", "author", "date_of_birth", "date_of_death", "n_char", "n_tok"]
date_cols = [i for i in azbhk_df.columns if re.search("pub_|birth_", i)]
all_cols = [i for i in azbhk_df.columns if re.search("all_", i)]
inc_cols = [i for i in azbhk_df.columns if re.search("_inc", i)]
abs_cols = [i for i in azbhk_df.columns if re.search("_abs", i)]
rel_cols = [i for i in azbhk_df.columns if re.search("_rel", i)]
z_cols = [i for i in azbhk_df.columns if re.search("_z", i)]
quant_cols = ["all_rel", "nt"]

all_df = azbhk_df[base_cols + date_cols + all_cols].replace("", np.nan).dropna(axis = 0, how =  "any").explode("all_inc")
h_bin_dict = {n:h for h in hk_dict.keys() for n in hk_dict[h]["Search Names"]}

all_df["h"] = [i[0] for i in all_df["all_inc"]]
all_df["h_bin"] = all_df["h"].map(h_bin_dict)
all_df["h_bin_season"] = [hk_dict[h]["Season"] for h in all_df["h_bin"]]
all_df["h_bin_bloom"] = [hk_dict[h]["In Bloom"] for h in all_df["h_bin"]]
all_df["h_bin_signifies"] = [hk_dict[h]["Signifies"] for h in all_df["h_bin"]]
all_df["tok"] = [i[1] for i in all_df["all_inc"]]
all_df["nt"] = [i/j for i,j in zip(all_df["tok"],all_df["n_tok"])]
all_df.to_csv("./outputs/all_df.csv")

#all_tables
by_genre = all_df[quant_cols + ["category_number"]].groupby(by = "category_number").agg("median")
by_author = all_df[quant_cols+ ["author"]].groupby(by = "author").agg("median")
by_h = all_df[quant_cols + ["h"]].groupby(by = "h").agg("median")
by_h_bin = all_df[quant_cols + ["h_bin"]].groupby(by = "h_bin").agg("median")

h_counts = all_df[["h"]].groupby(by = "h").agg("size").sort_values(ascending = False).to_frame()
h_bin_counts = all_df[["h_bin"]].groupby(by = "h_bin").agg("size").sort_values(ascending = False).to_frame()

by_h_bin_genre = all_df[quant_cols + ["h_bin", "category_number"]].groupby(by = ["h_bin", "category_number"]).agg(["median", "size"])
by_h_bin_author = all_df[quant_cols + ["h_bin", "author"]].groupby(by = ["h_bin", "author"]).agg(["median", "size"])

by_birth_year = all_df[quant_cols + ["birth_year"]].groupby(by = "birth_year").agg(["median", "size"])
by_birth_decade = all_df[quant_cols + ["birth_decade"]].groupby(by = "birth_decade").agg(["median", "size"])
by_birth_century = all_df[quant_cols + ["birth_century"]].groupby(by = "birth_century").agg(["median", "size"])
by_birth_jidai = all_df[quant_cols + ["birth_jidai"]].groupby(by = "birth_jidai").agg(["median", "size"])
by_birth_gannen = all_df[quant_cols + ["birth_gannen"]].groupby(by = "birth_gannen").agg(["median", "size"])
by_birth_month = all_df[quant_cols + ["birth_month"]].groupby(by = "birth_month").agg(["median", "size"])

by_h_bin_year = all_df[quant_cols+ ["h_bin", "birth_year"]].groupby(by = ["h_bin", "birth_year"]).agg(["median", "size"])
by_h_bin_decade = all_df[quant_cols+ ["h_bin", "birth_decade"]].groupby(by = ["h_bin", "birth_decade"]).agg(["median", "size"])
by_h_bin_century = all_df[quant_cols+ ["h_bin", "birth_century"]].groupby(by = ["h_bin", "birth_century"]).agg(["median", "size"])
by_h_bin_jidai = all_df[quant_cols+ ["h_bin", "birth_jidai"]].groupby(by = ["h_bin", "birth_jidai"]).agg(["median", "size"])
by_h_bin_gannen = all_df[quant_cols+ ["h_bin", "birth_gannen"]].groupby(by = ["h_bin", "birth_gannen"]).agg(["median", "size"])
by_h_bin_month = all_df[quant_cols+ ["h_bin", "birth_month"]].groupby(by = ["h_bin", "birth_month"]).agg(["median", "size"])

hk_df = pd.DataFrame(hk_dict).transpose()
hk_df.to_csv("./outputs/hk_df.csv")

out_list = [all_df, hk_df, genres, jidai, gannen,h_bin_counts,h_counts ,by_h_bin,by_h ,by_genre,by_h_bin_genre,by_author,by_h_bin_author ,by_h_bin_year]

with open("./data/analyses.pickle", 'wb') as f:
	pickle.dump(out_list, f)