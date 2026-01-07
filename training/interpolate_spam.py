import pandas as pd
import numpy as np

df = pd.read_csv("final_data_with_spam.csv")

def linear_interpolate(year, years, values):
    if year <= years[0]:
        return values[0]
    elif year >= years[-1]:
        return values[-1]
    else:
        # Find the interval that contains the year
        for i in range(len(years) - 1):
            if years[i] <= year <= years[i + 1]:
                x0, x1 = years[i], years[i + 1]
                y0, y1 = values[i], values[i + 1]
                # Linear interpolation formula
                return y0 + (y1 - y0) * (year - x0) / (x1 - x0)

new_rows=[]

for index, row in df.iterrows():
    year = row['HarvestYear']
    years = []
    values = []
    for year in [2000, 2005, 2010, 2017, 2020]:
        irr = row[f'{year}irr']
        if not pd.isna(irr):
            years.append(year)
            values.append(irr)
    if len(years) == 0:
        continue
    row['interpolated_irr'] = linear_interpolate(year, years, values)
    new_rows.append(row)

newdf = pd.DataFrame(new_rows)
newdf = newdf[newdf['HarvestYear'] > 2002]
newdf.drop(['2000irr', '2005irr', '2010irr', '2017irr', '2020irr'], inplace=True, axis=1)
newdf.to_csv('final_data_with_spam_interpolated.csv', index=False)