import pandas as pd

df = pd.read_csv("final_data_with_spam.csv")

df2017 = df.dropna(subset=["2017irr"])
df2017.drop(columns=['2010irr','2005irr','2000irr', '2020irr'], inplace=True)
df2017 = df2017.rename(columns={"2017irr": "irr"})
df2017 = df2017[df2017['HarvestYear'] == 2017]

df2010 = df.dropna(subset=["2010irr"])
df2010.drop(columns=['2017irr','2005irr','2000irr', '2020irr'], inplace=True)
df2010 = df2010.rename(columns={"2010irr": "irr"})
df2010 = df2010[df2010['HarvestYear'] == 2010]

df2020 = df.dropna(subset=["2020irr"])
df2020.drop(columns=['2017irr','2005irr','2000irr', '2010irr'], inplace=True)
df2020 = df2020.rename(columns={"2020irr": "irr"})
df2020 = df2020[df2020['HarvestYear'] == 2020]

combined_df = pd.concat([df2017, df2010, df2020], axis=0, ignore_index=True)

combined_df.to_csv("final_data_with_spam_only_2010_2017_2020.csv", index=False)