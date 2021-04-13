#!/usr/bin/env python
# coding: utf-8

# # Premier League Data Analysis
# ## Forrás: https://www.kaggle.com/saife245/english-premier-league
# ## Készítette: Szász Kristóf

# ## Az alábbi notebook a 2017-2018-as angol Premier League adatait, meccseit dolgozza fel, így az egyes csapatok, illetve maga a bajnokság tulajdonságait csak erre az időszakra értelmezem.
# 
# # Mit láthatunk ebben a notebookban?
#     - A csapatok hazai és idegenbeli győztes meccseinek összehasonlítását
#     - A csapatok mekkora részben nyernek meccseket az idény során hazai és idegenbeli pályán
#     - Mely csapatok voltak a legsportszerűbbek, illetve melyek a legszabálytalanabbak
#     - Melyik csapat találta el legtöbbször a kaput és melyik csapat lőtt a legtöbbször a kapura
#     - És végül hogyan alakult a bajnokság, azaz a tabella

# # FYI:
#  - Összesen 20 csapat van
#  - Minden csapatnak 38 mérkőzése van, 19 hazai pályán és 19 vendég pályán.

# # 1. Adatok importálása

# In[1]:


import pandas as pd
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
pd.set_option('display.max_columns', None)


# In[2]:


data = pd.read_csv('2017-18.csv')


# In[3]:


data.head()


# In[4]:


data.count()[0]


# # 2. Adatfeldolgozás

# ### Oszlopok leírása
# 
# - ``1. oszlop`` : Liga dimenziója - NEM KELL
# - ``Date`` : A mérkőzés dátuma
# - ``HomeTeam`` : Hazai csapat
# - ``AwayTeam`` : Vendég csapat
# - ``FTHG`` : Full Time Home Goals - Hazai csapat által lőtt gólok az egész mérkőzésen
# - ``FTAG`` : Full Time Away Goals - Vendég csapat által lőtt gólok az egész mérkőzésen
# - ``FTR`` : Full Time Result - Mérkőzés végeredménye
# - ``HTHG`` : Half Time Home Goals - Hazai csapat által lőtt gólok a félidőben 
# - ``HTAG`` : Half Time Away Goals - Vendég csapat által lőtt gólok a félidőben
# - ``HTR`` : Halt Time Result - Félidőben lévő végeredmény
# - ``Referee`` : Játékvezető - Valószínűleg nem kell
# - ``HS`` : Home team Shots - Hazai csapat kapuralövések 
# - ``AS`` : Away team Shots - Vendég csapat kapuralövések
# - ``HST`` : Home team Shots on Target - Hazai csapat kaput eltaláló lövések
# - ``AST`` : Away team Shots on Target - Vendég csapat kaput eltaláló lövések
# - ``HF`` : Home team Fouls committed - Hazai csapat által elkövetett szabálytalanságok
# - ``AF`` : Away team Fouls committed - Vendég csapat által elkövetett szabálytalanságok
# - ``HC`` : Home team Corners - Hazai csapat szögletrúgásai
# - ``AC`` : Away team Corners - Vendég csapat szögletrúgásai
# - ``HY`` : Home team Yellow cards - Hazai csapat sárgalapok száma
# - ``AY`` : Away team Yellow cards - Vendég csapat sárgalapok száma
# - ``HR`` : Home team Red cards - Hazai csapat piroslapok száma
# - ``AR`` : Away team Red cards - Vendég csapat piroslapok száma
# - ``Az utána lévő oszlopok számomra nem lényegesek, hiszen már így is elég sok adat áll rendelkezésemre.``

# ### Felesleges oszlopok eldobása

# In[5]:


data = data.iloc[:,1:23] # az utána lévő oszlopok nem kellenek
data = data.drop('Referee', axis = 1) # számomra nem fontos ki vezette a mérkőzést


# In[6]:


data.head()


# In[7]:


data.isnull().sum() # nincsenek NULL értékek


# # 3. Vizualizáció

# In[8]:


homeTeamWins = data[data.FTR == 'H'].groupby(data.HomeTeam).describe().FTHG['count'] # hányszor győzött egy csapat hazai pályán


# In[9]:


plt.figure(figsize=(30,10))
plt.plot(homeTeamWins, color = 'black', linewidth = 3)
plt.grid()


# In[10]:


awayTeamWins = data[data.FTR == 'A'].groupby(data.AwayTeam).describe().FTHG['count']


# In[11]:


plt.figure(figsize=(30,10))
plt.plot(awayTeamWins, color = 'black', linewidth = 3)
plt.grid()


# In[12]:


WinsData = pd.DataFrame({'homeWins':homeTeamWins, 'awayWins':awayTeamWins})


# In[13]:


HomeAndAwayWinsByTeams =  WinsData.plot(title = 'Hazai és idegenbeli győztes meccsek csapatonként', figsize = (20,8), grid = True, kind='bar', color = ['blue', 'red'])
HomeAndAwayWinsByTeams.set_xlabel("Csapat név")
HomeAndAwayWinsByTeams.set_ylabel("Meccsek száma")


# ### A csapatok hány százaléka nyert többször hazai pályán, mint idegenben?

# In[14]:


homeWinsPercentageByTeams = (WinsData[WinsData.homeWins > WinsData.awayWins].count() / WinsData.count()).homeWins * 100
homeWinsPercentageByTeams


# ### A csapatok hány százaléka nyert vagy játszott döntetlent több alkalommal hazai pályán, mint idegenben?

# In[15]:


homeWinsOrDrawPercentageByTeams = (WinsData[WinsData.homeWins >= WinsData.awayWins].count() / WinsData.count()).homeWins * 100
homeWinsOrDrawPercentageByTeams


# ### A csapatok hány százeléka nyert többször idegenben, mint hazai pályán?

# In[16]:


awayWinsPercentageByTeams = 100 - homeWinsOrDrawPercentageByTeams
awayWinsPercentageByTeams


# In[17]:


df = pd.DataFrame({'Stats': [homeWinsPercentageByTeams, (100 - homeWinsPercentageByTeams) - awayWinsPercentageByTeams , awayWinsPercentageByTeams]},
                  index=['Hazai pályán', 'Egyenlő', 'Idegenben'])
plot = df.plot.pie(y='Stats', figsize=(5, 5), title = 'Hol nyernek több meccset a csapatok az idény során?', colors = ['green', 'orange', 'red'])


# In[18]:


FoulsAsHomeTeam = data.HF.groupby(data.HomeTeam).sum()


# In[19]:


FoulsAsAwayTeam = data.AF.groupby(data.AwayTeam).sum()


# In[20]:


FoulsData = pd.DataFrame({'FoulsAsHomeTeam':FoulsAsHomeTeam, 'FoulsAsAwayTeam':FoulsAsAwayTeam})


# In[21]:


HomeAndAwayFoulsByTeams =  FoulsData.plot(title = 'Hazai és idegenbeli szabálytalanságok csapatonként', figsize = (20,8), grid = True, kind='bar', color = ['blue','red'])
HomeAndAwayFoulsByTeams.set_xlabel("Csapat név")
HomeAndAwayFoulsByTeams.set_ylabel("Szabálytalanságok száma")


# In[22]:


SummarizedFoulsByTeams = FoulsData.FoulsAsHomeTeam + FoulsData.FoulsAsAwayTeam


# ### Legkevesebb szabálytalanságot elkövető csapatok

# In[23]:


SummarizedFoulsByTeams.sort_values().head()


# ### Legtöbb szabálytalanságot elkövető csapatok

# In[24]:


SummarizedFoulsByTeams.sort_values(ascending = False).head()


# ### Kapuralövések csapatonként

# In[25]:


ShotsAsHomeTeam = data.HS.groupby(data.HomeTeam).sum()


# In[26]:


ShotsAsAwayTeam = data.AS.groupby(data.AwayTeam).sum()


# In[27]:


ShotsData = pd.DataFrame({'ShotsAsHomeTeam':ShotsAsHomeTeam, 'ShotsAsAwayTeam':ShotsAsAwayTeam})


# In[28]:


ShotsDataByTeams =  ShotsData.plot(title = 'Hazai és idegenbeli kapura lövések csapatonként', figsize = (20,8), grid = True, kind='bar', color = ['blue', 'red'])
ShotsDataByTeams.set_xlabel("Csapat név")
ShotsDataByTeams.set_ylabel("Kapura lövések csapatonként")


# In[29]:


SummarizedShotsData = ShotsData.ShotsAsHomeTeam + ShotsData.ShotsAsAwayTeam


# ### A csapatok hány százaléka lőtt az idény során az ellenfél kapujára többször amikor hazai pályán szerepelt, mint amikor idegenben

# In[30]:


(ShotsData[ShotsData.ShotsAsHomeTeam > ShotsData.ShotsAsAwayTeam].count() / ShotsData.count()).ShotsAsHomeTeam * 100


# ### Kaput eltaláló lövések csapatonként

# In[31]:


ShotsOnTargetAsHomeTeam = data.HST.groupby(data.HomeTeam).sum()


# In[32]:


ShotsOnTargetAsAwayTeam = data.AST.groupby(data.AwayTeam).sum()


# In[33]:


ShotsOnTargetData = pd.DataFrame({'ShotsOnTargetAsHomeTeam':ShotsOnTargetAsHomeTeam, 'ShotsOnTargetAsAwayTeam':ShotsOnTargetAsAwayTeam})


# In[34]:


ShotsOnTargetsByTeams =  ShotsOnTargetData.plot(title = 'Hazai és idegenbeli kaput eltaláló lövések csapatonként', figsize = (20,8), grid = True, kind='bar', color = ['blue', 'red'])
ShotsOnTargetsByTeams.set_xlabel("Csapat név")
ShotsOnTargetsByTeams.set_ylabel("Kaput eltaláló lövések csapatonként")


# ### A csapatok hány százaléka találja el többször hazai csapatként az ellenfél kapuját, mint vendég csapatként

# In[35]:


((ShotsOnTargetData[ShotsOnTargetData.ShotsOnTargetAsHomeTeam > ShotsOnTargetData.ShotsOnTargetAsAwayTeam].count() / ShotsOnTargetData.count()) * 100).ShotsOnTargetAsHomeTeam


# In[36]:


SummarizedShotsOnTargetData = ShotsOnTargetData.ShotsOnTargetAsHomeTeam + ShotsOnTargetData.ShotsOnTargetAsAwayTeam


# ### Gólok száma csapatonként

# In[37]:


FullTimeGoalsAsHomeTeam = data.FTHG.groupby(data.HomeTeam).sum()


# In[38]:


FullTimeGoalsAsAwayTeam = data.FTAG.groupby(data.AwayTeam).sum()


# In[39]:


FullTimeGoalsData = pd.DataFrame({'FullTimeGoalsAsHomeTeam':FullTimeGoalsAsHomeTeam, 'FullTimeGoalsAsAwayTeam':FullTimeGoalsAsAwayTeam})


# In[40]:


FullTimeGoalsDataByTeams =  FullTimeGoalsData.plot(title = 'Hazai és idegenbeli gólok csapatonként', figsize = (20,8), grid = True, kind='bar', color = ['blue', 'red'])
FullTimeGoalsDataByTeams.set_xlabel("Csapat név")
FullTimeGoalsDataByTeams.set_ylabel("Gólok csapatonként")


# ### A csapatok hány százaléka szerez több gólt hazai csapatként, mint vendég csapatként 

# In[41]:


((FullTimeGoalsData[FullTimeGoalsData.FullTimeGoalsAsHomeTeam > FullTimeGoalsData.FullTimeGoalsAsAwayTeam].count() / FullTimeGoalsData.count()) * 100).FullTimeGoalsAsHomeTeam


# In[42]:


SummarizedFullTimeGoalsData = FullTimeGoalsData.FullTimeGoalsAsHomeTeam + FullTimeGoalsData.FullTimeGoalsAsAwayTeam
SummarizedFullTimeGoalsData


# In[43]:


Shots_ShotsOnTarget_Goals = pd.DataFrame({'SummarizedShotsData':SummarizedShotsData, 
                                          'SummarizedShotsOnTargetData':SummarizedShotsOnTargetData, 
                                          'SummarizedFullTimeGoalsData':SummarizedFullTimeGoalsData})


# In[44]:


Shots_ShotsOnTarget_GoalsPlot =  Shots_ShotsOnTarget_Goals.plot(title = 'Kapura lövések, kaput eltaláló lövések és gólok csapatonként', figsize = (20,8), grid = True, kind='bar', color = ['green','yellow','red'])
Shots_ShotsOnTarget_GoalsPlot.set_xlabel("Csapat név")
Shots_ShotsOnTarget_GoalsPlot.set_ylabel("Kapuralövések/Kaput eltaláló lövések/Gólok")


# ### Ahogy látható a kapuralövés egyenesen arányos a kaput eltaláló lövésekkel és a gólok számával, ezért jön ki az eredményül, hogy a legtöbbet kapuralövő csapatok találták el legtöbbször a kaput, illetve ezek a csapatok is szerezték a legtöbb gólt az idény során

# In[45]:


SummarizedShotsData.sort_values(ascending = False).head()


# In[46]:


SummarizedShotsOnTargetData.sort_values(ascending = False).head()


# In[47]:


SummarizedFullTimeGoalsData.sort_values(ascending = False).head()


# ### Viszont ez még nem feltétlenül jelenti azt, hogy arányaiban tekintve is ők a legjobb csapatok, ezért ha elosztjuk a gólszámot a kapuralövésekkel, láthatjuk, hogy mely csapatok lőnek a legpontosabban kapura vagy legalábbis melyik csapatok lőnek inkább akkor, amikor úgy érzik gólt tudnak szerezni

# In[48]:


((SummarizedFullTimeGoalsData / SummarizedShotsData) * 100).sort_values(ascending = False).head()


# ### Az West Ham és Leicester eddig nem szerepelt egyszer sem a legjobb csapatok között az adatokat tekintve viszont azt látható, hogy a gólszám/összes lövés esetén igen jól szerepeltek, a többi csapat eddig is a legaktívabbak között volt

# ### És új meglepetés emberként az Arsenal is felküzdötte magát a legjobbak közé, sőt ebben a statisztikában ő is lett a  legjobb, tehát ha kaput eltaláló lövésekből ekkora százalékban szereznek gólt az alábbi csapatok, ami számomra meglepően magas

# In[49]:


((SummarizedShotsOnTargetData / SummarizedShotsData) * 100).sort_values(ascending = False).head()


# # Tabella

# In[52]:


teams = data.HomeTeam.unique()
teams.sort()


# In[53]:


LeagueTable = pd.DataFrame({'Team':teams, 'Points':0}, index = teams)
##LeagueTable.sort_values('Points')
LeagueTable.index = np.arange(1, len(LeagueTable) + 1)


# In[54]:


def leaugeTablePoints(dataframe):
    if dataframe['FTR'] == 'H':
        LeagueTable.at[LeagueTable.loc[LeagueTable.Team == dataframe.HomeTeam].index[0], 'Points'] += 3
    elif dataframe['FTR'] == 'A':
        LeagueTable.at[LeagueTable.loc[LeagueTable.Team == dataframe.AwayTeam].index[0], 'Points'] += 3
    elif dataframe['FTR'] == 'D':
        LeagueTable.at[LeagueTable.loc[LeagueTable.Team == dataframe.HomeTeam].index[0], 'Points'] += 1
        LeagueTable.at[LeagueTable.loc[LeagueTable.Team == dataframe.AwayTeam].index[0], 'Points'] += 1


# In[55]:


data.apply(leaugeTablePoints, axis = 1)


# In[56]:


LeagueTable = LeagueTable.sort_values('Points', ascending = False)
LeagueTable['Rank'] = range(1,21)


# In[57]:


LeagueTable.style.hide_index()


# ### Egy kis érdekesség

# In[58]:


data.apply(min, axis = 0)


# In[59]:


data.apply(max, axis = 0)


# In[60]:


data[data.FTHG == 7]


# https://www.google.com/search?q=2017+18+man+city+stoke&oq=2017+18+man+city+stoke&aqs=chrome..69i57j33i22i29i30.6206j0j9&sourceid=chrome&ie=UTF-8#sie=m;/g/11ggb123dt;2;/m/02_tc;dt;fp;1;;
