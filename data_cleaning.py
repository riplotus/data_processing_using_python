"""
Created at 16:21 on 03.07.20

@author: lingsun
"""
import matplotlib.pyplot as plt
import pandas as pd
thefts=pd.read_excel("./thefts_and_pop.xls",sheet_name=0)
pop = pd.read_excel("./thefts_and_pop.xls",sheet_name=1)

#print(thefts.head())
#print(pop.head())

# create a column "key" from "State" name + "County" name.
thefts["key"]=thefts["State"]+thefts["County"]
thefts["key"]=thefts["key"].str.lower()
pop["key"]=pop["State"]+pop["County"]
pop["key"]=pop["key"].str.lower()

# merge the two data frames based on the common column "key".
thefts_pop = pd.merge(thefts, pop,left_on="key",right_on="key")
#print(thefts_pop.head())

# creat a new column, thefts per 10k population.
thefts_pop["Thefts per 10,000"] = thefts_pop["Motor vehicle thefts"]*(10000/thefts_pop[2014])
print(thefts_pop.head())

# plot the value of the column
thefts_pop["Thefts per 10,000"].plot()
plt.show()

# see the index of the maximal value
print(thefts_pop["Thefts per 10,000"].idxmax())

#see the maximal value
print(thefts_pop["Thefts per 10,000"].max())

# see the exact row where the maximal value locates.
print(thefts_pop.iloc[thefts_pop["Thefts per 10,000"].idxmax()])

# save the data to a csv / excel file.
thefts_pop.to_excel("thefts_pop_output.xls",index=None) # no index.
