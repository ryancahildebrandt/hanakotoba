#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
Created on Thu Nov 11 08:43:14 PM EST 2021 

author: Ryan Hildebrandt 
"""

# %% Doc setup
import bs4
import pandas as pd
import pickle
import pykakasi
import re
import requests

kks = pykakasi.kakasi()

# %% funcs
def scrape_hk(target_url, start_regex, start_n, end_regex, end_n):
	hkn_p = requests.get(target_url)
	hkn_s = bs4.BeautifulSoup(hkn_p.content, "html.parser", parse_only = bs4.SoupStrainer("p"))
	hkn_l = [i.get_text() for i in hkn_s if i.get_text() != ""]
	start_i = hkn_l.index(start_regex, start_n)+1
	end_i = hkn_l.index(end_regex, end_n)
	hkn_l = hkn_l[start_i:end_i]
	hkn_list.append(hkn_l)

def brackets_to_list(in_str):
	out_list = [re.sub("[」「 ]", "", i) for i in in_str.split("」「")]
	return out_list

def variant_meanings(in_list, target_variant):
	target_item = [i for i in in_list if re.search(f"≪{target_variant}≫", i)]
	target_item = re.sub(f"≪{target_variant}≫","", target_item[0]) if len(target_item) != 0 else "" 
	out = brackets_to_list(target_item)
	return out

def all_scripts(in_str):
	in_orig = "".join([i["orig"] for i in kks.convert(in_str)])
	in_hira = "".join([i["hira"] for i in kks.convert(in_str)])
	in_kat = "".join([i["kana"] for i in kks.convert(in_str)])
	out_list = [in_orig, in_hira, in_kat]
	return out_list

def scrape_search_names(in_list):
	in_list = [all_scripts(i) for i in in_list]
	in_list = [i for j in in_list for i in j]
	in_str = ",".join(in_list)
	out_list = re.split("[,（）、/ ]", in_str)
	out_list = list(set([i for i in out_list if i]))
	return out_list

# %% azb readin
azb_df = pd.read_csv("./data/aozora_corpus_en.csv")

# %% hanakotoba scrape
hkn_url_a = "https://hananokotoba.com/hananonamae/"
hkn_urls = [
"https://hananokotoba.com/hananonamae-2/",
"https://hananokotoba.com/hananonamae-3/",
"https://hananokotoba.com/hananonamae-4/",
"https://hananokotoba.com/hananonamae-5/",
"https://hananokotoba.com/hananonamae-6/",
"https://hananokotoba.com/hananonamae-7/",
"https://hananokotoba.com/hananonamae-8/",
"https://hananokotoba.com/hananonamae-9/",
"https://hananokotoba.com/hananonamae-10/",
"https://hananokotoba.com/hananonamae-11/",
"https://hananokotoba.com/hananonamae-12/",
"https://hananokotoba.com/hananonamae-13/"
]

hkn_list = []

scrape_hk(hkn_url_a, "・1月の花\u3000・2月の花\u3000・3月の花\u3000・4月の花\u3000・5月の花\u3000・6月の花\u3000・7月の花\u3000・8月の花\u3000・9月の花\u3000・10月の花\u3000・11月の花\u3000・12月の花", 0, "\xa0", 10)

for h in hkn_urls:
	scrape_hk(h, "\xa0\n", 0, "\xa0", 0)

hkn_list = "".join([";;".join(i) for i in hkn_list]).split(";;\n")
hkn_list = [re.sub(";;", "\n", i) for i in hkn_list]
hkn_list = [re.sub("\u3000", "", i) for i in hkn_list]
hkn_list = [re.sub("※", "", i) for i in hkn_list]
hkn_list = [i.split("\n") for i in hkn_list]
hkn_dict = {
[re.sub(" \| 詳細 →", "", i) for i in hkn_list[ind] if re.search("詳細", i)][0]:{
"Index":ind, 
"Family":[re.sub("科・属名：(.*?科)?(（.*?）)?(.*?属)?(（.*?）)?", "\g<1>", i) for i in hkn_list[ind] if re.search("^科・属名：", i)][0],
"Genus":[re.sub("科・属名：(.*?科)?(（.*?）)?(.*?属)?(（.*?）)?", "\g<3>", i) for i in hkn_list[ind] if re.search("^科・属名：", i)][0],
"Scientific Name":[re.search("学名：(.*)", i).group(1) for i in hkn_list[ind] if re.search("^学名：", i)][0],
"Japanese Name":[re.search("和名：(.*)", i).group(1) for i in hkn_list[ind] if re.search("^和名：", i)][0],
"Other Name":[re.sub("別名.(.*?)", "\g<1>", i) for i in hkn_list[ind] if re.search("^別名：", i)],
"Western Name":[re.sub("英名.(.*?)", "\g<1>", i) for i in hkn_list[ind] if re.search("^英名：", i) and re.sub("英名.(.*?)", "\g<1>", i) != "無"],
"Derivation":"".join(hkn_list[ind][hkn_list[ind].index("花の名前の由来")+1:hkn_list[ind].index([i for i in hkn_list[ind] if re.search("^旬の季節：", i)][0])]) if '花の名前の由来' in hkn_list[ind] else "",
"Season":[re.search("旬の季節：(.*)", i).group(1) for i in hkn_list[ind] if re.search("^旬の季節：", i)][0],
"In Bloom":[re.sub("開花時期.(.*?)", "\g<1>", i) for i in hkn_list[ind] if re.search("^開花時期：", i)],
"Signifies":[brackets_to_list(re.search("花言葉（全般）：(.*)", i).group(1)) for i in hkn_list[ind] if re.search("^花言葉（全般）：", i)][0]
} for ind,h in enumerate(hkn_list)}

for h in hkn_dict:
	hkn_dict[h]["Search Names"] = scrape_search_names([*hkn_dict[h]["Other Name"], hkn_dict[h]["Japanese Name"]])

hki_page = requests.get("https://hananokotoba.com/hanakotoba-ichiran/")
hki_soup = bs4.BeautifulSoup(hki_page.content, "html.parser", parse_only = bs4.SoupStrainer("td"))
hki_list = [i.get_text() for i in hki_soup][:-2]
hki_list = [i.split("\n") for i in hki_list]

variants = list(set(re.findall("≪.*?≫", "".join(["".join(i) for i in hki_list]))))
variants = [re.sub("≪|≫", "", i) for i in variants]

hki_dict = {
[re.sub(" \| 詳細 →", "",i) for i in hki_list[ind] if re.search("詳細", i)][0]:{
"Signifies":[brackets_to_list(re.sub("【全般】", "", i))[0] for i in hki_list[ind] if re.search("【全般】", i)],
"Variants":[i for i in hki_list[ind] if re.search("≪.*≫", i)]
} for ind,h in enumerate(hki_list)}

for h in hki_dict:
	for v in variants:
		hki_dict[h][v] = variant_meanings(hki_dict[h]["Variants"], v)

# %% updating individual fields
hki_dict["アヤメ"] = hki_dict.pop("アイリス（アヤメ）")
hki_dict.pop("アヤメ（アイリス）")
hkn_dict["アヤメ"] = hkn_dict.pop("アヤメ（アイリス）")
hkn_dict["アヤメ"]["Other Name"] = "アイリス"

hki_dict["エゾギク"] = hki_dict.pop("エゾギク / アスター")
hki_dict.pop("アスター / エゾギク")
hkn_dict["エゾギク"] = hkn_dict.pop("エゾギク（アスター）")

hki_dict["コルチカム"] = hki_dict.pop("イヌサフラン（コルチカム）")
hki_dict.pop("コルチカム（イヌサフラン）")
hkn_dict["コルチカム"]["Other Name"] = hkn_dict["コルチカム"]["Other Name"].append("イヌサフラン")

hki_dict["プラタナス"] = hki_dict.pop("プラタナス（スズカケノキ）")
hki_dict.pop("スズカケノキ（プラタナス）")
hkn_dict["プラタナス"]["Other Name"] = hkn_dict["プラタナス"]["Other Name"].append("スズカケノキ")

hki_dict["ミスミソウ"] = hki_dict.pop("ミスミソウ（ユキワリソウ）")
hki_dict.pop("ユキワリソウ（ミスミソウ）")
hkn_dict["ミスミソウ"]["Other Name"] = hkn_dict["ミスミソウ"]["Other Name"].append("ユキワリソウ")

hki_dict["サイネリア"] = hki_dict.pop("サイネリア（シネラリア）")
hki_dict.pop("シネラリア（サイネリア）")
hkn_dict["サイネリア"] = hkn_dict.pop("シネラリア（サイネリア）")
hkn_dict["サイネリア"]["Other Name"] = hkn_dict["サイネリア"]["Other Name"].append("シネラリア")

hki_dict["アカシア"] = hki_dict.pop("ミモザ（アカシア）")
hkn_dict["アカシア"] = hkn_dict.pop("ミモザ（アカシア）")

hki_dict[""] = {i:[""] for i in hki_dict["アヤメ"].keys()}
hkn_dict[""] = {i:[""] for i in hkn_dict["アヤメ"].keys()}

# %% combine
hk_names = list(set().union(hki_dict, hkn_dict))

hk_dict = {}
for h in hk_names:
	if h in hkn_dict.keys() and h in hki_dict.keys():
		hk_dict[h] = hkn_dict[h] | hki_dict[h]
	elif h in hkn_dict.keys() and h not in hki_dict.keys():
		hk_dict[h] = hkn_dict[h] | hki_dict[""]
	elif h not in hkn_dict.keys() and h in hki_dict.keys():
		hk_dict[h] = hkn_dict[""] | hki_dict[h]

# %% export
#pd.DataFrame.from_dict(data = hki_dict, orient = "index").to_csv("./data/hki_df.csv")
#d.DataFrame.from_dict(data = hkn_dict, orient = "index").to_csv("./data/hkn_df.csv")
#pd.DataFrame.from_dict(data = hk_dict, orient = "index").to_csv("./data/hk_df.csv")

azb_df = azb_df.iloc[:10]
main_texts = azb_df["main_text"]
meta_df = azb_df.drop("main_text", axis = 1)

with open("./data/meta_df.pickle", 'wb') as f:
	pickle.dump(meta_df, f)

with open("./data/main_texts.pickle", 'wb') as f:
	pickle.dump(main_texts, f)

with open("./data/hk_dicts.pickle", 'wb') as f:
	pickle.dump([hki_dict, hkn_dict, hk_dict], f)

'''
index:指数
family:科
genus:属
scientific name:学名
japanese name:和名
other name:別名
western:英名
derivation:由来
season:旬の季節
in bloom:開花時期
signifies:花言葉（全般）
'''
