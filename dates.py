#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
Created on Sun May  1 01:10:22 PM EDT 2022 

author: Ryan Hildebrandt 
"""

# %% Doc setup
import dateutil as du
import itertools as it
import numpy as np
import pandas as pd
import pickle
import re

from astropy.time import Time

#date things
#eras https://kids.kiddle.co/List_of_Japanese_eras and wikipedia
#pandas datetime throws out of bound datetime for early authors, using astropy
jidai = pd.read_csv("./時代.csv")
jidai["終"] = [i-1 for i in jidai.iloc[1:,0].tolist() + [2023]]
jidai_dict = {j:{"start" : i, "end" : k} for i,j,k in jidai.values}

gannen = pd.read_csv("./元年.csv")
gannen["終"] = [i-1 for i in gannen.iloc[1:,0].tolist() + [2023]]
gannen_dict = {j:{"start" : i, "end" : k} for i,j,k in gannen.values}

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

by_pub_year = all_df[quant_cols + ["pub_year"]].groupby(by = "pub_year").agg(["mean", "median", "size"])
by_pub_decade = all_df[quant_cols + ["pub_decade"]].groupby(by = "pub_decade").agg(["mean", "median", "size"])
by_pub_century = all_df[quant_cols + ["pub_century"]].groupby(by = "pub_century").agg(["mean", "median", "size"])
by_pub_jidai = all_df[quant_cols + ["pub_jidai"]].groupby(by = "pub_jidai").agg(["mean", "median", "size"])
by_pub_gannen = all_df[quant_cols + ["pub_gannen"]].groupby(by = "pub_gannen").agg(["mean", "median", "size"])
by_pub_month = all_df[quant_cols + ["pub_month"]].groupby(by = "pub_month").agg(["mean", "median", "size"])

by_birth_year = all_df[quant_cols + ["birth_year"]].groupby(by = "birth_year").agg(["mean", "median", "size"])

#subset to year>1500
by_birth_decade = all_df[quant_cols + ["birth_decade"]][all_df["birth_year"] >= 1500].groupby(by = "birth_decade").agg(["mean", "median", "size"])
by_birth_century = all_df[quant_cols + ["birth_century"]][all_df["birth_year"] >= 1500].groupby(by = "birth_century").agg(["mean", "median", "size"])
by_birth_jidai = all_df[quant_cols + ["birth_jidai"]][all_df["birth_year"] >= 1500].groupby(by = "birth_jidai").agg(["mean", "median", "size"])
by_birth_gannen = all_df[quant_cols + ["birth_gannen"]][all_df["birth_year"] >= 1500].groupby(by = "birth_gannen").agg(["mean", "median", "size"])
by_birth_month = all_df[quant_cols + ["birth_month"]][all_df["birth_year"] >= 1500].groupby(by = "birth_month").agg(["mean", "median", "size"])

by_h_bin_decade = all_df[quant_cols+ ["h_bin", "birth_decade"]].groupby(by = ["h_bin", "birth_decade"]).agg(["mean", "median", "size"])
by_h_bin_century = all_df[quant_cols+ ["h_bin", "birth_century"]].groupby(by = ["h_bin", "birth_century"]).agg(["mean", "median", "size"])
by_h_bin_jidai = all_df[quant_cols+ ["h_bin", "birth_jidai"]].groupby(by = ["h_bin", "birth_jidai"]).agg(["mean", "median", "size"])
by_h_bin_gannen = all_df[quant_cols+ ["h_bin", "birth_gannen"]].groupby(by = ["h_bin", "birth_gannen"]).agg(["mean", "median", "size"])
by_h_bin_month = all_df[quant_cols+ ["h_bin", "birth_month"]].groupby(by = ["h_bin", "birth_month"]).agg(["mean", "median", "size"])

#many effects seem to be author based
#limit to authors and themes/meanings because removing authors because they contribute a lot kinda kills the data

