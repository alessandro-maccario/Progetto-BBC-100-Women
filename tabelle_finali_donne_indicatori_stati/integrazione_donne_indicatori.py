import pandas as pd
import numpy as np

"""**Nomi e codici stati**"""

# nomi stati e codici stati (ma per cosa lo usiamo in questo notebook??? per le ministre e le parlamentari
# e per il labour percentage)
# https://www.iban.com/country-codes
names_codes = pd.read_excel('names_codes.xlsx')

"""**Scaricamento classifiche donne BBC 2015 e 2020**"""

# classifica BBC donne 2015
# https://www.bbc.co.uk/news/special/2015/newsspec_12497/content/english/index.html?v=0.1.24&hostid=www.bbc.com&hostUrl=https%3A%2F%2Fwww.bbc.com%2Fnews%2Fworld-34745739&iframeUID=responsive-iframe-61225031&onbbcdomain=true#facewall_15
bbc2015 = pd.read_excel('BBC100Women_2015_originale.xlsx')
bbc2015.drop(columns='\n', inplace=True)
bbc2015.rename(columns={'nationality':'Country'}, inplace=True)

# classifica BBC donne 2019
# https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-12-08/women.csv
bbc2019= pd.read_csv('data_BBC100Women_2019.csv', sep=';')
bbc2019.rename(columns={'role':'job'}, inplace=True)

"""**Scaricamento dati indicatori dei paesi**"""

# global gender gap ci mancano gli anni in mezzo
# https://reports.weforum.org/global-gender-gap-report-2020/the-global-gender-gap-index-2020-rankings/
# sul sito del wef, la data di pubblicazione del report del 2020 è dicembre 2019, quindi assumiamo che i dati si riferiscano al 2019
ggg2019= pd.read_csv('gender_gap_2020.csv', sep=';')

# https://reports.weforum.org/global-gender-gap-report-2015/rankings/
ggg2015= pd.read_csv('gender_gap_2015.csv', sep=';')

# pil pro capite 1980 - 2025
# https://www.imf.org/external/datamapper/NGDPDPC@WEO/OEMDC/ADVEC/WEOWORLD
gdp_capite = pd.read_excel('gdp_percapita_ful.xls')
gdp_capite.rename(columns={'GDP per capita, current prices\n (U.S. dollars per capita)':'Country'}, inplace=True)

# pil 1980 - 2025
#https://www.imf.org/external/datamapper/NGDPD@WEO/OEMDC/ADVEC/WEOWORLD
gdp= pd.read_excel('gdp_full.xls')
gdp.rename(columns={'GDP, current prices (Billions of U.S. dollars)':'Country'}, inplace=True)

# rapporto donne uomini lavoro 2011 - 2019
#https://databank.worldbank.org/source/gender-statistics/preview/on
labour_percentage_raw= pd.read_csv('labour_percentage.csv')
labour_percentage_raw.rename(columns={'Country Code':'3-digit'}, inplace=True)
labour_percentage = pd.merge(labour_percentage_raw, names_codes, on='3-digit')[['Country', '2015 [YR2015]', '2019 [YR2019]']]
labour_percentage.rename(columns={'2015 [YR2015]':'labour_percentage_2015',  '2019 [YR2019]':'labour_percentage_2019'}, inplace=True)
labour_percentage['labour_percentage_2015']=pd.to_numeric(labour_percentage['labour_percentage_2015'], errors='coerce').round(2)
labour_percentage['labour_percentage_2019']=pd.to_numeric(labour_percentage['labour_percentage_2019'], errors='coerce').round(2)


# human development index
# http://hdr.undp.org/en/content/human-development-index-hdi
hdi= pd.read_csv('../../../Telegram Desktop/telegram download/Human_Development_Index.csv', sep=';')

"""**Creazione tabelle finali per 2015 e 2019**"""

# TABELLA FINALE 2019
gdp_gdpcapite= pd.merge(gdp, gdp_capite, how='outer', on='Country')
gdp_gdpcapite.rename(columns={'2019_x':'gdp', '2019_y':'gdp_pro_capita'}, inplace=True)
gdp_gdpcapite=gdp_gdpcapite[['Country', 'gdp', 'gdp_pro_capita']]

gdp_gdpcapite_labor= pd.merge(gdp_gdpcapite,labour_percentage, how='outer', on='Country')
gdp_gdpcapite_labor.rename(columns={'labour_percentage_2019':'labour_percentage'}, inplace=True)
gdp_gdpcapite_labor=gdp_gdpcapite_labor[['Country', 'gdp', 'gdp_pro_capita', 'labour_percentage']]

gdp_gdpcapite_labor_ggg= pd.merge(gdp_gdpcapite_labor, ggg2019, how='outer',left_on='Country', right_on='country')
gdp_gdpcapite_labor_ggg.rename(columns={'score':'gender_gap'}, inplace=True)
gdp_gdpcapite_labor_ggg.drop(columns='country', inplace=True)

gdp_gdpcapite_labor_ggg_hdi= pd.merge(gdp_gdpcapite_labor_ggg, hdi, how='outer', on='Country')
gdp_gdpcapite_labor_ggg_hdi.rename(columns={'2019':'hdi'}, inplace=True)
gdp_gdpcapite_labor_ggg_hdi= gdp_gdpcapite_labor_ggg_hdi[['Country', 'gdp', 'gdp_pro_capita', 'labour_percentage','gender_gap', 'hdi']]

tot_19= pd.merge(gdp_gdpcapite_labor_ggg_hdi, bbc2019, how='outer', on='Country')

tot_19['year']=2019
# totale2019.to_csv('integrazione_2019.csv')

# TABELLA FINALE 2015
gdp_gdpcapite1= pd.merge(gdp, gdp_capite, how='outer', on='Country')
gdp_gdpcapite1.rename(columns={'2015_x':'gdp', '2015_y':'gdp_pro_capita'}, inplace=True)
gdp_gdpcapite1=gdp_gdpcapite1[['Country', 'gdp', 'gdp_pro_capita']]

gdp_gdpcapite_labor1= pd.merge(gdp_gdpcapite1,labour_percentage, how='outer', on='Country')
gdp_gdpcapite_labor1.rename(columns={'labour_percentage_2015':'labour_percentage'}, inplace=True)
gdp_gdpcapite_labor1=gdp_gdpcapite_labor1[['Country', 'gdp', 'gdp_pro_capita', 'labour_percentage']]

gdp_gdpcapite_labor_ggg1= pd.merge(gdp_gdpcapite_labor1, ggg2015, how='outer',left_on='Country', right_on='Economy')
gdp_gdpcapite_labor_ggg1.rename(columns={'Score':'gender_gap'}, inplace=True)
gdp_gdpcapite_labor_ggg1.drop(columns='Economy', inplace=True)

gdp_gdpcapite_labor_ggg_hdi1= pd.merge(gdp_gdpcapite_labor_ggg1, hdi, how='outer', on='Country')
gdp_gdpcapite_labor_ggg_hdi1.rename(columns={'2015':'hdi'}, inplace=True)
gdp_gdpcapite_labor_ggg_hdi1= gdp_gdpcapite_labor_ggg_hdi1[['Country', 'gdp', 'gdp_pro_capita', 'labour_percentage','gender_gap', 'hdi']]

tot_15= pd.merge(gdp_gdpcapite_labor_ggg_hdi1, bbc2015 , how='outer', on='Country')

tot_15['year']=2015
# totale2015.to_csv('integrazione_2015.csv')

totale = pd.concat([tot_15, tot_19])
totale1= totale.dropna(subset=['Country'])
totale2= totale1[['Country', 'year','gdp', 'gdp_pro_capita', 'labour_percentage', 'gender_gap', 'hdi', 'name']]
totale2.to_csv('Stati_donne.csv')

# pivot - per viz

gdp_gdpcapite_labor_ggg_hdi1= gdp_gdpcapite_labor_ggg_hdi1[['Country', 'gdp', 'gdp_pro_capita', 'labour_percentage','gender_gap', 'hdi']]
tot_15=gdp_gdpcapite_labor_ggg_hdi1
tot_15['year']=2015

gdp_gdpcapite_labor_ggg_hdi= gdp_gdpcapite_labor_ggg_hdi[['Country', 'gdp', 'gdp_pro_capita', 'labour_percentage','gender_gap', 'hdi']]
tot_19= gdp_gdpcapite_labor_ggg_hdi
tot_19['year']=2019

totale = pd.concat([tot_15, tot_19])
totale1= totale.dropna(subset=['Country'])

bbc2015['year']=2015
bbc2019['year']=2019

final= pd.melt(totale1, id_vars=['Country', 'year'])
final1= pd.merge(final, bbc2015, how='outer', on=['Country', 'year'])
final2= pd.merge(final1, bbc2019, how='outer', on=['Country', 'year'])
final3= final2[['Country', 'year', 'variable', 'value', 'name_x', 'name_y']]
final3['name'] = final3['name_x'].fillna('') + final3['name_y'].fillna('')
final_final=final3[['Country', 'year', 'variable', 'value', 'name']]
pd.to_numeric(final_final['value'], errors='coerce')
final_final.to_csv('stati_pivot_donne.csv')