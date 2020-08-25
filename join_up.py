import pandas as pd

keywords = ["smoking","cigarette-smoking","pipe-smoking","cigar-smoking"]

#Making a DataFrame for every keyword
dfs = []
for keyword in keywords:
    df = pd.read_csv(f"{keyword}_list.csv", skipfooter = 1)
    df.insert(1,f"{keyword}",True)
    keywords_cpy = keywords.copy()
    keywords_cpy.remove(keyword)
    for keyword_cpy in keywords_cpy:
        df.insert(2,f"{keyword_cpy}",False)
    df = df[["id","smoking","cigarette-smoking","pipe-smoking","cigar-smoking"]]
    dfs.append(df)

#Joinining the DataFrames, while accounting for duplicates
Movies = dfs[0].copy()

k = 1
while k < len(dfs):
    df = dfs[k].copy()
    for i in df.id:
        jdx = 0
        for j in Movies.id:
            if i == j:
                Movies.loc[jdx,f"{keywords[k]}"] = True
            jdx += 1
    Movies = Movies[["id","smoking","cigarette-smoking","pipe-smoking","cigar-smoking"]]
    Movies = Movies.append(df, ignore_index = True)
    Movies = Movies.drop_duplicates(subset = ["id"], keep= "first")
    k += 1

Movies.to_csv("joined_list.csv",index = False)

