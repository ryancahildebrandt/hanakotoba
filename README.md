# Literature in Bloom

---

[*Open*](https://gitpod.io/#https://github.com/ryancahildebrandt/hanakotoba) *in gitpod*

## *Purpose*

A project to explore 花言葉 (hanakotoba, lit. flower language) in Japanese and other literary corpora.

---

## Dataset
The dataset used for the current project was pulled from the following: 
- [Aozora Bunko Corpus](https://www.kaggle.com/datasets/ryancahildebrandt/azbcorpus) for Japanese full text works
- [Hanakotoba](https://hananokotoba.com) for flower names, translations, and associated characteristics
- [Wikipedia](https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC%E5%8D%81%E9%80%B2%E5%88%86%E9%A1%9E%E6%B3%95) for conversions of Japanese decimal classification codes (分類番号) 
- [Wikipedia](https://en.wikipedia.org/wiki/Japanese_era_name) for a list of major Japanese eras (時代)
- [This page](https://kids.kiddle.co/List_of_Japanese_eras) for a list of sub-eras (元年)
*Some of these didn't end up being necessary for the main project but are included with the accompanying code for genre and date conversions*

---

## Outputs
+ The main [report](https://datapane.com/reports/dkjbvwk/literature-in-bloom/), compiled with datapane and also in [html](./outputs/hanakotoba_rprt.html) format
+ Historical era dataframe : [Jidai.csv](./outputs/jidai.csv)
+ Sub-era dataframe : [Gannen.csv](./outputs/gannen.csv)
+ Japanese genre code dataframe : [Genres.csv](./outputs/genres.csv)
+ Dataframe of all flowers/plants and associated characteristics : [Hk_df.csv](./outputs/hk_df.csv)
+ Dataframe with all text metainfo, calculated date columns, and tagged flower occurences with locations in the text : [All_df.csv](./outputs/all_df.csv)
