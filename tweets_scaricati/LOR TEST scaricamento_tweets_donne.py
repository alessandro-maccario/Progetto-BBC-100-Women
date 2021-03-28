import csv
import time
import json
import twint
import os.path
import datetime
import simplejson
import nest_asyncio
import pandas as pd
from datetime import datetime
from datetime import timedelta
from jsonmerge import merge


def scaricamento_tweets(until, since, changing, remaining_days, complete_tweets_db):

    while True:
        time.sleep(1)
        print("-----------------------------------------------")
        print('\nDobbiamo scaricare fino al giorno: ', since.strftime('%Y-%m-%d'))
        print('\nStiamo scaricando i tweets del giorno: ', (until - timedelta(days=1)).strftime('%Y-%m-%d'))
        print('\nQuindi tutti quei tweets compresi nel seguente intervallo temporale:  {} <-------> {}'.format(changing, until))
        print('\nRimangono da scaricare {} giorni'.format(remaining_days))
        print("\nSTART COLLECTING...")

        c = twint.Config()
        c.Search = query
        c.Store_csv = True
        c.Since = changing.strftime('%Y-%m-%d %H:%M:%S')
        c.Until = until.strftime('%Y-%m-%d %H:%M:%S')
        c.Pandas= True
        c.Count= True
        c.Hide_output= True
        # c.Store_json = True
        c.User_full= True

        twint.run.Search(c)

        # Importo i dati giornalieri nel dataframe completo
        complete_tweets_db = complete_tweets_db.append(twint.storage.panda.Tweets_df)

        if int(str(changing-since)[0]) == 0: # significa che abbiamo considerati tutti i giorni del nostro arco temporale generale, quindi il ciclo di ricerca deve stopparsi
            break

        # Cambio finestra temporale a livello giornaliero
        changing = changing - timedelta(days = 1) # sarebbe il since
        until = until - timedelta(days = 1)

        if str(changing-since).split()[0] == '0:00:00': # necessario per evitare errore stampa output ultimo giorno
            remaining_days = 0
        else:
            remaining_days = int(str(changing-since).split()[0])

        nest_asyncio.apply() # resetto loop di ricerca cosi non sembra un attacco dos

        print('\n', end='\r')

        # eliminazione dei duplicati
        complete_tweets_db_new_no_duplicates = complete_tweets_db[~complete_tweets_db.index.duplicated()]

    return complete_tweets_db_new_no_duplicates


# lista donne
df_lista_donne = pd.read_csv("tweets donne Lorenzo/tabella_sistemata_3_restante.csv", sep=',')
df_lista_donne.columns


df_lista_donne['hashtag_list'] = df_lista_donne.hashtag.str.split()
df_lista_ridotta = df_lista_donne[["id", "name", "username_twitter", "hashtag_list", "year"]]

# creazione struttura json da riempire con i tweets pre e post classifica
donne_dictionary = {}

for donna in df_lista_ridotta.itertuples():
  if donna[1] not in donne_dictionary:

    donne_dictionary[donna[1]] = {
        "tweets": {
            "pre-classifica": [],
            "post-classifica": []
        }
    }


# Download dei tweets a partire dalla donna
for riga in df_lista_ridotta.itertuples():
    print("*"*30)
    print("NOME DONNA: ", riga.name)
    # creo un nuovo dataset completo
    complete_tweets_db = pd.DataFrame()
    #time.sleep(10)
    # impostazione date
    nest_asyncio.apply()  # Blocco eventuali loop di ricerca in corso

    if riga.year == 2015:
        # prima finestra
        until1 = datetime(2015, 11, 14, 00, 00, 00)
        until1 = until1 + timedelta(days=1)  # per considerare tutte le 24 ore del primo giorno
        since1 = datetime(2015, 11, 1, 00, 00, 00)
        changing1 = until1 - timedelta(days=1)
        remaining_days1 = int(str(changing1 - since1).split()[0])

        # seconda finestra
        until2 = datetime(2015, 12, 1, 00, 00, 00)
        until2 = until2 + timedelta(days=1)  # per considerare tutte le 24 ore del primo giorno
        since2 = datetime(2015, 11, 15, 00, 00, 00)
        changing2 = until2 - timedelta(days=1)
        remaining_days2 = int(str(changing2 - since2).split()[0])

    else:
        # prima finestra
        until1 = datetime(2019, 10, 15, 00, 00, 00)
        until1 = until1 + timedelta(days=1)  # per considerare tutte le 24 ore del primo giorno
        since1 = datetime(2019, 8, 1, 00, 00, 00)
        changing1 = until1 - timedelta(days=1)
        remaining_days1 = int(str(changing1 - since1).split()[0])

        # seconda finestra
        until2 = datetime(2020, 1, 1, 00, 00, 00)
        until2 = until2 + timedelta(days=1)  # per considerare tutte le 24 ore del primo giorno
        since2 = datetime(2019, 10, 16, 00, 00, 00)
        changing2 = until2 - timedelta(days=1)
        remaining_days2 = int(str(changing2 - since2).split()[0])

    #-------------------------------------------------------------------------------------------------
    presence_name = True
    name = riga.name
    id_donna = riga.id
    # user_mention_bbc = "@BBC100Women"
    # hashtags_bbc = "#BBC100Women OR #BBC100women OR #bbc100women OR #Bbc100Women OR #bbc100WOMEN OR #bBc100women OR #BBC100WOMEN OR #100women"
    # query_bbc = "{} OR {}".format(user_mention_bbc, hashtags_bbc)

    presence_username_twitter = False
    if (type(riga.username_twitter)) is not float and riga.username_twitter != '':
        user_mention = riga.username_twitter
        presence_username_twitter = True

    presence_hashtag = False
    if (type(riga.hashtag_list)) is not float:
        hashtags_considerati = ''

        for element in riga.hashtag_list:
            hashtags_considerati = hashtags_considerati + element + ' OR '
        hashtags_considerati = hashtags_considerati + query_bbc
        presence_hashtag = True
    else:
        hashtags_considerati = query_bbc

    if presence_username_twitter == False:
        query = "{} AND ({})".format(name, hashtags_considerati)
    else:
        query= "{} OR ({} AND ({}))".format(user_mention, name, hashtags_considerati)
    #-------------------------------------------------------------------------------------------------

    # chiave = riga.name
    # id_donna = riga.id
    # user_mention = riga.username_twitter
    #
    # user_mention_bbc = "@BBC100Women"
    # hashtags_bbc = "#BBC100Women OR #BBC100women OR #bbc100women OR #Bbc100Women OR #bbc100WOMEN OR #bBc100women OR #BBC100WOMEN"
    # query_bbc = "{} OR {}".format(user_mention_bbc, hashtags_bbc)
    #
    # # hashtags_considerati_lista = riga.hashtag_list.split()
    # hashtags_considerati = ''
    # for element in riga.hashtag_list:
    #     hashtags_considerati = hashtags_considerati + element + ' OR '
    #
    # hashtags_considerati = hashtags_considerati + query_bbc
    #
    # query = "({} OR ({} AND ({})))".format(user_mention, chiave, hashtags_considerati)  # @todo: secondo me vedere se user_mention != '' equivale a vedere se è false
    print('query: ', query)

    print('sopra df1')
    df1 = scaricamento_tweets(until1, since1, changing1, remaining_days1, complete_tweets_db)
    if not df1.empty:
        print('non sono empty')
        df1.set_index('id', inplace=True)
        df1= df1[['date', 'tweet', 'language', 'hashtags', 'user_id', 'username', 'name', 'nlikes', 'nreplies', 'nretweets']]

        for tweet in df1.itertuples():
            print("3) ------------------ SONO QUI! ------------------")
            if tweet not in donne_dictionary[id_donna]["tweets"]["pre-classifica"]:
                donne_dictionary[id_donna]["tweets"]["pre-classifica"].append(tweet)

    print('sopra df2')
    df2 = scaricamento_tweets(until2, since2, changing2, remaining_days2, complete_tweets_db)
    if not df2.empty:
        print('non sono empty')
        df2.set_index('id', inplace=True)
        df2 = df2[['date', 'tweet', 'language', 'hashtags', 'user_id', 'username', 'name', 'nlikes', 'nreplies', 'nretweets']]

        for tweet in df2.itertuples():

            print("4) ------------------ SONO QUI! ------------------")
            if tweet not in donne_dictionary[id_donna]["tweets"]["post-classifica"]:
                donne_dictionary[id_donna]["tweets"]["post-classifica"].append(tweet)


with open('poooo.json', 'w', encoding="UTF-8") as f:
    simplejson.dump(donne_dictionary, f, ignore_nan=True)

print(donne_dictionary)

with open('parte1.json') as f:
    data1 = json.load(f)

with open('parte2.json') as f:
    data2 = json.load(f)

with open('parte3.json') as f:
    data3 = json.load(f)

with open('parte4.json') as f:
    data4 = json.load(f)

with open('parte5.json') as f:
    data5 = json.load(f)

# unisco parti - Lorenzo
output_final_merging = merge(data1, data2)
output_final_merging = merge(output_final_merging, data3)
output_final_merging = merge(output_final_merging, data4)
output_final_merging = merge(output_final_merging, data5)


#unisco greta
with open('greta.json') as f:
    data6 = json.load(f)
output_final_merging = merge(output_final_merging, data6)

#unisco le ultime due donne
with open('ultime_due.json') as f:
    data6 = json.load(f)
output_final_merging = merge(output_final_merging, data6)



with open('merge_lorenzo_completo.json', 'w', encoding="UTF-8") as f:
    simplejson.dump(output_final_merging, f, ignore_nan=True)
# merge ignorante dovrebbe essere uguale, ma senza greta e le ultime due donne