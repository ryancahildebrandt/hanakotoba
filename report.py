#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
Created on Sat Apr 23 08:09:52 PM EDT 2022 

author: Ryan Hildebrandt 
"""

# %% Doc setup
import altair as alt
import datapane as dp
import pickle

dp.enable_logging()

with open("./data/analyses.pickle", "rb") as f:
	all_df, hk_df, genres, jidai, gannen, h_bin_counts,h_counts ,by_h_bin,by_h ,by_genre,by_h_bin_genre,by_author,by_h_bin_author ,by_h_bin_year = pickle.load(f)

alt.data_transformers.disable_max_rows()
alt.themes.enable("dark")

#all_viz
h_bin_genre_p_heatmap = alt.Chart(by_h_bin_genre["all_rel"]["median"].to_frame().reset_index().sort_values(by = "median",ascending = False)[:20]).mark_rect().encode(
    x = alt.X('h_bin:N'),
    y = alt.Y('category_number:N'),
    color = alt.Color('median:Q')
).interactive().properties(
    title="Proportion of Flower Occurrences by Genre (Top 20)",
    width='container'
)

h_bin_genre_n_heatmap = alt.Chart(by_h_bin_genre["all_rel"]["size"].to_frame().reset_index().sort_values(by = "size",ascending = False)[:20]).mark_rect().encode(
    x = alt.X('h_bin:N'),
    y = alt.Y('category_number:N'),
    color = alt.Color('size:Q')
).interactive().properties(
    title="Number of Flower Occurrences by Genre (Top 20)",
    width='container'
)

h_bin_author_p_heatmap = alt.Chart(by_h_bin_author["all_rel"]["median"].to_frame().reset_index().sort_values(by = "median",ascending = False)[:20]).mark_rect().encode(
    x = alt.X('h_bin:N'),
    y = alt.Y('author:N'),
    color = alt.Color('median:Q')
).interactive().properties(
    title="Proportion of Flower Occurrences by Author (Top 20)",
    width='container'
)

h_bin_author_n_heatmap = alt.Chart(by_h_bin_author["all_rel"]["size"].to_frame().reset_index().sort_values(by = "size",ascending = False)[:20]).mark_rect().encode(
    x = alt.X('h_bin:N'),
    y = alt.Y('author:N'),
    color = alt.Color('size:Q')
).interactive().properties(
    title="Number of Flower Occurrences by Author (Top 20)",
    width='container'
)

h_bin_year_n_line = alt.Chart(by_h_bin_year["all_rel"]["size"].reset_index()).mark_line().encode(
    x='birth_year:T',
    y='size:Q',
    color="h_bin:N",
    tooltip = [alt.Tooltip("birth_year:T"),
               alt.Tooltip("size:Q"),
               alt.Tooltip("h_bin:N")]
).interactive().properties(
title = "Number of Occurrences by Year",
width='container'
)

h_bin_year_p_line = alt.Chart(by_h_bin_year["all_rel"]["median"].reset_index()).mark_line().encode(
    x='birth_year:T',
    y='median:Q',
    color='h_bin:N',
    tooltip = [alt.Tooltip("birth_year:T"),
               alt.Tooltip("size:Q"),
               alt.Tooltip("h_bin:N")]
).interactive().properties(
title = "Proportion of Occurrences by Year",
width='container'
)

nt_dist = alt.Chart(all_df[["nt"]]).transform_density(
    "nt",
    as_=["nt", "density"],
).mark_area(
opacity=0.3
).encode(
    x="nt:Q",
    y='density:Q',
).interactive().properties(
title = "Distribution of Occurrences by Narrative Time",
width='container'
)

nt_dist_by_h_bin = alt.Chart(all_df[["nt","h_bin"]]).mark_area(
    opacity=0.3
).encode(
    alt.X('nt:Q', bin=alt.Bin(maxbins=100)),
    alt.Y('count()', stack=None),
    alt.Color('h_bin:N')
).interactive().properties(
title = "Distribution of Occurrences for Each Flower by Narrative Time",
width='container'
)

all_abs_dist = alt.Chart(all_df[["all_abs"]]).transform_density(
    "all_abs",
    as_=["all_abs", "density"],
).mark_area(
opacity=0.3
).encode(
    x="all_abs:Q",
    y='density:Q',
).interactive().properties(
title = "Distribution of Number of Occurrences per Text",
width='container'
)

all_rel_dist = alt.Chart(all_df[["all_rel"]]).transform_density(
    "all_rel",
    as_=["all_rel", "density"],
).mark_area(
opacity=0.3
).encode(
    x="all_rel:Q",
    y='density:Q',
).interactive().properties(
title = "Distribution of Proportion of Occurrences per Text",
width='container'
)

h_bin_year_ntok_scatter = alt.Chart(all_df[["birth_year","n_tok", "all_abs", "h_bin"]]).mark_point(filled=True).encode(
    alt.X("birth_year:Q"),
    alt.Y("n_tok:Q"),
    alt.Size("all_abs:Q"),
    alt.Color("h_bin:N", legend=None),
    alt.OpacityValue(0.5),
    tooltip = [alt.Tooltip("birth_year:T"),
               alt.Tooltip("n_tok:Q"),
               alt.Tooltip("all_abs:Q"),
               alt.Tooltip("h_bin:N")
               ]
               ).interactive().properties(
title = "Occurrences by Year, Text Length, and Flower",
width='container'
)

rprt = dp.Report(
	dp.Text("""
# Literature in Bloom
#### *Exploring 花言葉 in Japanese (and other) literary corpora*
花言葉 (hanakotoba, lit. flower language) is the selective use of flowers to represent specific meanings, messages, or ideas. These references can appear in and out of literature, including names, gifts/accompaniments to letters, and elements of setting. 花言葉 shows up in many literary traditions in some form or another, but has a particularly widespread usage across Japanese history.

---

## Dataset
The dataset used for the current project was pulled from the following: 
- [Aozora Bunko Corpus](https://www.kaggle.com/datasets/ryancahildebrandt/azbcorpus) for Japanese full text works
- [Hanakotoba](https://hananokotoba.com) for flower names, translations, and associated characteristics
- [Wikipedia](https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC%E5%8D%81%E9%80%B2%E5%88%86%E9%A1%9E%E6%B3%95) for conversions of Japanese decimal classification codes (分類番号) 
- [Wikipedia](https://en.wikipedia.org/wiki/Japanese_era_name) for a list of major Japanese eras (時代)
- [This page](https://kids.kiddle.co/List_of_Japanese_eras) for a list of sub-eras (元年)
*Some of these didn't end up being necessary for the main project but are included with the accompanying code for genre and date conversions*
		"""),
	dp.DataTable(all_df),
	dp.Text("""
---

## Approach

### 花言葉
This project builds off previous work I'd done with the Aozora Bunko corpus above, which consists of a large body of literary work from Japan as well as works not initially published in Japanese that have been translated. As such, essentially all of the initial work of finding and compiling the corpus had been taken care of, and the first thing to do was to find some decently comprehensive source of flowers and their associated meanings in the Japanese literary world. Hanakotoba.com (also listed above) provided the most comprehensive list I could find. 

Within this website, there's a page (or at least a blurb) for each flower/plant that includes the following:

- Family
- Genus
- Scientific Name
- Japanese Name
- Other Name
- Western Name
- Name Derivation
- Associated Season
- Dates In Bloom
- Significance

As well as some additional information for color/varietal variations where appropriate. 
		"""),
	dp.DataTable(hk_df),
	dp.Text("""
After scraping this information into a manageable dictionary form and making a couple manual adjustments to fix some formatting inconsistencies in the source page, the next step was to identify the in-text occurrences of each flower in the corpus.

### Tagging
One of the challenges of written Japanese is that it doesn't rely on punctuation or whitespace to denote word boundaries. This means that just searching for the exact text of a flower name may work perfectly fine for some examples (栗/chestnut, which doesn't pop up super frequently outside of actually talking about chestnuts), but not so well for other examples (め/pampas grass, which could be talking about the plant in question but could also appear in any number of words on its own). This is fixed by tokenizing all of the texts before trying to search through them, keeping only instances which match a full token rather than any appearance anywhere in the text. This leads to some overlooked Occurrences in the case of names or proper nouns that may have only one kanji related to a particular flower, but saves many more false positive appearances of a single kana anywhere in a word that may *happen* to be another name for a flower.

With each appropriate appearance of a given flower name, the number of the matching token is also recorded to allow for calculation of narrative time, basically a standardized measure of how far along in a given text a match was found.

### Themes, Seasons, and Other Characteristics
The "meaning" of each flower in the dataset is split into its name derivation, its associated season/blooming period, and associated characteristics or themes. For the sake of simplicity, flower variants and alternative names were binned into their most common name. For example, all instances of 松、まつ、and マツ are lumped under the same name and stored as マツ (in katakana) for consistency. From this standardized name, associated themes and meanings can be referenced as needed and substituted in for any given appearance of the target flower.

### Text Metainfo

#### Authors
To make a long series of exploratory analyses and scatter plots much shorter, the vast majority of trends in the data seemed to be author-driven. That is to say, date and genre effects were small or masked enough to be not reasonably interpretable when taking authorship into account. This makes sense when we step back from the numbers for a moment and understand that literature isn't just something that *happens*, and is a collection of works put out by individuals with their own styles, goals, and backgrounds. Removing an author or work with an exceptionally influential body of work may allow for a more even comparison of other authors or works, but does much more damage insofar as it removes a very *real* aspect of the data as a whole.

As such, much of the date and genre related work was done before this realization and was not included for most of the interpretations below. The code and explanation of approaches is still included, mostly just to have some record of the **inordinate** amount of time spent getting these dates in line.

#### Genres
The Aozora Bunko corpus included Japanese decimal classification codes (分類番号) for each work and needed to be converted into some manner of readable genre. Genres were pulled unceremoniously (good ol' copy & paste) from Wikipedia, manually edited to csv format, and mapped on to the first genre code for each work. The csv is included here as an additional resource.
		"""),
	dp.DataTable(genres),
	dp.Text("""
#### Dates
Date conversions were decidedly much nastier to iron out. Among the notable issues faced were:

- BC dates causing issues with pandas & numpy & base & dateutil datetime formats 
- Incomplete/missing dates for many authors
- Dates provided in 時代/元年 or the beginning/end of a particular century
- Converting ymd type dates **into** 時代/元年 for comparison's sake

Thankfully much of this was eventually sorted out, but resentfully much of it was rendered useless by the realization that individual authors, not the shifting of literary tastes over time, seemed to be the main driver behind any kind of time based effects. Nonetheless, the 時代 and 元年 files are included in case this kind of thing is useful for anyone out there.
"""),
	dp.DataTable(jidai),
	dp.DataTable(gannen),
	dp.Text("""
---

## Distributions & Tables
*Unless otherwise noted, the median was used for aggregation in the following results, given the skewness of most measures in the data*

### Narrative Time
Aggregating across all flowers, Occurrences in narrative time form a pretty uniform distribution. Splitting this by flower results in a chaotic spread of Occurrences, but with some appreciable peaks for a good number of flowers. This may be another result of large proportions of Occurrences for a given flower coming from a small number of texts.
"""),
	dp.Group(
		dp.Plot(nt_dist),
		dp.Plot(nt_dist_by_h_bin),
		columns = 2
		),
	dp.Text("""
### Occurrences per Text
The distribution of Occurrences per text is heavily right skewed, with most texts having less than 60 (and a slight bump at 90-100). As far as the proportion of each text classifiable as 花言葉, the distribution has an extremly limited range almost entirely below 1.5% of total text length (by tokens).
		"""),
	dp.Plot(all_abs_dist),
	dp.Plot(all_rel_dist),
	dp.Text("""
### By Flower
*Notable conclusions from the flowers, author, and genre aggregations are outlined below in the "Some Qualitative Results" section, and as such the tables are presented here without comment*
		"""),
	dp.Group(
		dp.DataTable(h_bin_counts),
		dp.DataTable(h_counts),
		columns = 2
		),
	dp.Group(
		dp.DataTable(by_h_bin),
		dp.DataTable(by_h),
		columns = 2
		),
	dp.Text("""
### By Genre
		"""),
	dp.Group(
		dp.DataTable(by_genre),
		dp.DataTable(by_h_bin_genre),
		columns = 2
		),
	dp.Text("""
### By Author
		"""),
	dp.Group(
		dp.DataTable(by_author),
		dp.DataTable(by_h_bin_author),
		columns = 2
		),
	dp.Text("""
### By Birth Year
		"""),
	dp.Plot(h_bin_year_p_line),
	dp.Plot(h_bin_year_n_line),
	dp.Plot(h_bin_year_ntok_scatter),
	dp.Text("""
---

## Some Qualitative Results
Kodō Nomura (野村胡堂) has a disproportunate contribution with マツ (1192) and キリ (646). While マツ shows up in other authors works, キリ comes almost exclusively from nomura. This naturally carries over into short story genre, in which Nomura was a prolific author.
		"""),
	dp.Group(
		dp.Plot(h_bin_author_n_heatmap),
		dp.Plot(h_bin_genre_n_heatmap),
		columns = 2
	),
	dp.Text("""
When looking at the relative proportion of flowers mentioned as compared to text length, the results are at least slightly more balanced. ナノハナ and ススキ dominate here, with the biggest contributions coming from Bochō Yamamura (山村暮鳥) with a median ナノハナ occurrence of .1485 and Chuyo Sakurama (桜間中庸) with a median ススキ occurrence of .0862. 

Again and perhaps unsurprisingly, poetry has a widespread usage of 花言葉 spread across a range of flowers. Likely due to Yamamura's contributions, essays also have a relatively high proportion of 花言葉, though these examples tend to be more concentrated (in ナノハナ and a handful of others).
		"""),
	dp.Group(
		dp.Plot(h_bin_author_p_heatmap),
		dp.Plot(h_bin_genre_p_heatmap),
		columns = 2
	),
	dp.Text("""
And a closing note on those connotations that are sort of the whole point of 花言葉 in *any* language, I'll at least include the connotations for each of the most popular flowers/plants, and I encourage you to look through the results above and find a flower or connotation you're particularly interested in and see where it shows up!

| Flower | Signifies | Translation |
| --- | --- | --- |
| マツ | 不老長寿 | longevity |
| ススキ | 活力 | vitality |
| キリ | 高尚 | nobility |
| ナノハナ | 快活 | lightheartedness |
		"""),
	dp.Text("""# 完了""")
	)

rprt.save(path = './outputs/hanakotoba_rprt.html', open=True)
#rprt.upload(name='Literature in Bloom', open = True, publicly_visible = True)
#https://datapane.com/reports/dkjbvwk/literature-in-bloom/