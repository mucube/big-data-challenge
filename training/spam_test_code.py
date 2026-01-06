import pandas as pd

df = pd.read_csv("final_data_with_spam.csv")

df2017 = df.dropna(subset=["2017irr"])
df2017.drop(columns=['2010irr','2005irr','2000irr'], inplace=True)
df2017 = df2017.rename(columns={"2017irr": "irr"})

df2010 = df.dropna(subset=["2010irr"])
df2010.drop(columns=['2017irr','2005irr','2000irr'], inplace=True)
df2010 = df2010.rename(columns={"2010irr": "irr"})

df2005 = df.dropna(subset=["2005irr"])
df2005.drop(columns=['2010irr','2017irr','2000irr'], inplace=True)
df2005 = df2005.rename(columns={"2005irr": "irr"})

combined_df = pd.concat([df2005, df2010, df2017], axis=0, ignore_index=True)

combined_df.to_csv("final_data_with_spam_only_2005_2010_2017.csv", index=False)