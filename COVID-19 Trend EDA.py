#COVID 19 DATASET EDA BY USING PYTHON

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime

#Uploading the dataset which has covid cases details in INDIA
covid_df = pd.read_csv("covid_19_india.csv")

#EDA on covid_19_india.csv file
covid_df.info()
covid_df.describe()

#removing the some columns such as data time and cases nation wise

covid_df.drop(["Sno", "Time", "ConfirmedIndianNational"	,"ConfirmedForeignNational"], inplace=True, axis = 1)

#converting the format of date
covid_df['Date']=pd.to_datetime(covid_df['Date'], format = '%Y-%m-%d')



#Calculatin Active cases

covid_df['Active_cases']= (covid_df['Confirmed']-(covid_df['Cured']+covid_df['Deaths']))
covid_df.tail()

#now we are creating the pivot table.

statewise = pd.pivot_table(covid_df, values = ["Cured",	"Deaths",	"Confirmed"], index = "State/UnionTerritory", aggfunc= max)
display(statewise)

# @title Deaths

from matplotlib import pyplot as plt
statewise['Deaths'].plot(kind='hist', bins=20, title='Deaths')
plt.gca().spines[['top', 'right',]].set_visible(False)

#recovery and mortality rate
statewise["Recovery"] = (statewise["Cured"]/statewise["Confirmed"])*100
statewise["mortality"] = (statewise["Deaths"]/statewise["Confirmed"])*100
statewise = statewise.sort_values(by= "Confirmed", ascending=False)
statewise.style.background_gradient(cmap= "cubehelix")   #cmap = for choosing the colour of pivot table it is a function of Maplotlib




#top 10 active cases states
top_10_active_cases= covid_df.groupby(by='State/UnionTerritory').max()[['Active_cases', 'Date']].sort_values(by=['Active_cases'], ascending = False).reset_index()


#figure size
fig = plt.figure(figsize=(16,9))
#figure title
plt.title("Top 10 states with active cases in India", size = 25)
#adding axis
ax = sns.barplot(data = top_10_active_cases.iloc[:10], y = "Active_cases", x = "State/UnionTerritory", linewidth = 2, edgecolor = "blue")
#yaha pe hum jo axix k labels hai unko define ka rahe hai taki sb mix na ho
plt.xlabel("States")
plt.ylabel("Total Active Cases")
plt.show()

#top states with high number of deaths
top_10_deaths_states= covid_df.groupby(by='State/UnionTerritory').max()[["Deaths", "Date"]].sort_values(by = ["Deaths"], ascending= False).reset_index()

fig = plt.figure(figsize=(16,9))
plt.title("Statewise Deaths in India due to COVID-19", size = 25)
ax=sns.barplot(data= top_10_deaths_states[:10], y = "Deaths", x= "State/UnionTerritory", linewidth = 2, edgecolor = "Pink")
plt.xlabel("State/UnionTerritory")
plt.ylabel("Deaths")
plt.show()

#growth trend conclusion 
fig = plt.figure(figsize = (12, 6))
ax = sns.lineplot(data = covid_df[covid_df['State/UnionTerritory'].isin(['Maharashtra', 'Kerala', 'Karnataka', 'Tamil Nadu', 'Uttar Pradesh'])], x = 'Date', y= 'Active_cases', hue = 'State/UnionTerritory')
ax.set_title("Top 5 Affected states in India", size = 16)

                                                             #Now we will wok with second sheet
 
##Uploading the dataset which has vaccination details in INDIA

covid_df2=pd.read_csv('/content/covid_vaccine_statewise.csv')
covid_df2.info()
covid_df2.describe()
covid_df2.rename(columns = {"Updated On" :" Vaccine_Date"}, inplace = True)
Vaccination=covid_df2.drop(columns=['Sputnik V (Doses Administered)',
       'AEFI', '18-44 Years (Doses Administered)',
       '45-60 Years (Doses Administered)', '60+ Years (Doses Administered)',
       '18-44 Years(Individuals Vaccinated)',
       '45-60 Years(Individuals Vaccinated)',
       '60+ Years(Individuals Vaccinated)'] , axis =1)

#Vaccination

#now we will create pipeplot for checkin vaccination of male and female fo rthis we will use ploty lib
male= Vaccination["Male(Individuals Vaccinated)"].sum()
female= Vaccination["Female(Individuals Vaccinated)"].sum()
px.pie(names=["Male","Female"], values = [male, female], title = "Male and Female")

Vaccination.rename(columns ={"Total Individuals Vaccinated" : "Total"}, inplace = True)

#most vaccinated states
max_vac = Vaccination.groupby("State")["Total"].sum().to_frame("Total")
max_vac = max_vac.sort_values("Total", ascending= False)[:5]

fig = plt.figure(figsize =(10,5))
plt.title("top 5 Vaccinated tates in India", size =20)
x =sns.barplot(data=max_vac.iloc[:10],y = max_vac.Total, x =max_vac.index, linewidth= 2, edgecolor ="purple")
plt.xlabel("States")
plt.ylabel("Vaccination")
plt.show()