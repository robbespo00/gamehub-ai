import sklearn as skl
import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
import random
import json
import pickle

def registerVote(vote: bool) -> bool:
    try:

        dataFrame = pd.read_csv("./buffer.csv")
        dataFrame['Vote'] = vote
        dataFrameVotes = pd.read_csv("./votes.csv")
        username = dataFrame.iloc[0].Username
        flag = False

        for i in range(0, len(dataFrameVotes['Username'])):
            if(dataFrameVotes['Username'][i] == username):
                dataFrameVotes['Vote'][i] = vote
                flag = True

        print(dataFrameVotes)
        if(not flag):
            dataFrame.to_csv("./votes.csv", index=False, mode='a', header=False)
        else:
            dataFrameVotes.to_csv("./votes.csv", index=False, header=True)

        return True
    except:
        return False


def getDictionaryFromFile(filename: str) -> dict:
    # Read a map of countries in a file
    try:
        with open(filename, 'r') as file:
            dictionary = json.load(file)
            return dictionary
    except FileNotFoundError:
        return {}


def encodeCountry(dataFrame):
    countryList = ['IT', 'US', 'CA', 'BA', 'AU', 'NZ', 'DE', 'UM', 'RU', 'SE', 'JP', 'AF', 'AL',
                   'DZ', 'AS', 'AD', 'AO', 'GB', 'ES', 'PT', 'AR', 'BE', 'BR', 'NO', 'FR', 'CH',
                   'CZ', 'SI', 'ZA', 'KR', 'LK', 'SS', 'SG', 'TN', 'TK', 'UA', 'AE', 'UY', 'VN',
                   'ZW', 'ZM', 'YE', 'TM']

    # Take dictionary from file
    #encodingCountry = getDictionaryFromFile('Map.json')
    # Set starting value
    #j = len(encodingCountry)
    # Cycle to put random values and encode each country
    for i in range(0, len(dataFrame['Country'])):
        newRow = countryList[random.randint(0, len(countryList) - 1)]
        if (pd.isnull(dataFrame['Country'][i])):
            dataFrame['Country'][i] = newRow
        #value = dataFrame['Country'][i]
        #if (value not in encodingCountry):
        #    encodingCountry[value] = j
        #   j += 1
        #dataFrame['Country'][i] = encodingCountry[value]

    # Save a map of countries in a file
    #with open('Map.json', 'w') as file:
    #    json.dump(encodingCountry, file)


def main():
    # Open file .csv
    dataFrame = pd.read_csv('../../Desktop/datasetRaw.csv')

    # Remove useless columns
    dataFrame.drop(columns=['communityvisibilitystate'], axis=1, inplace=True)
    dataFrame.drop(columns=['profilestate'], axis=1, inplace=True)
    dataFrame.drop(columns=['cityid'], axis=1, inplace=True)
    dataFrame.drop(columns=['loccityid'], axis=1, inplace=True)
    dataFrame.drop(columns=['personastate'], axis=1, inplace=True)

    # Rename columns
    dataFrame.rename(columns={'steamid': 'Id', 'personaname': 'Username', 'loccountrycode': 'Country'}, inplace=True)

    # Random country code generator
    encodeCountry(dataFrame)

    # Retrieve values to format
    categories = dataFrame['Categories']
    genres = dataFrame['Genres']
    developers = dataFrame['Developers']
    publishers = dataFrame['Publishers']
    countries = dataFrame['Country']

    # Create multilabelbinarizer
    one_hot = MultiLabelBinarizer()

    # Settings option to display dataset without '...'
    # pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)

    # Format values in to One Hot Encode
    resultCategories = pd.DataFrame(one_hot.fit_transform(categories.dropna().str.split(',')), columns=one_hot.classes_,
                                    index=dataFrame.index)
    resultCategories = resultCategories.add_prefix('Ctg_')

    resultGenres = pd.DataFrame(one_hot.fit_transform(genres.dropna().str.split(',')), columns=one_hot.classes_,
                                index=dataFrame.index)
    resultGenres = resultGenres.add_prefix('Tag_')

    resultDevelopers = pd.DataFrame(one_hot.fit_transform(developers.dropna().str.split(',')), columns=one_hot.classes_,
                                    index=dataFrame.index)
    resultDevelopers = resultDevelopers.add_prefix('Dvp_')

    resultPublishers = pd.DataFrame(one_hot.fit_transform(publishers.dropna().str.split(',')), columns=one_hot.classes_,
                                    index=dataFrame.index)
    resultPublishers = resultPublishers.add_prefix('Pbl_')

    resultCountries = pd.DataFrame(one_hot.fit_transform(countries.dropna().str.split(' ')), columns=one_hot.classes_,
                                   index=dataFrame.index)

    # Merge tables in to one
    result = pd.merge(dataFrame, resultCategories, on=dataFrame.index)
    result.drop(columns=['key_0', 'Categories'], axis=1, inplace=True)

    result = pd.merge(result, resultGenres, on=dataFrame.index)
    result.drop(columns=['key_0', 'Genres'], axis=1, inplace=True)

    result = pd.merge(result, resultDevelopers, on=dataFrame.index)
    result.drop(columns=['key_0', 'Developers'], axis=1, inplace=True)

    result = pd.merge(result, resultPublishers, on=dataFrame.index)
    result.drop(columns=['key_0', 'Publishers'], axis=1, inplace=True)

    result = pd.merge(result, resultCountries, on=dataFrame.index)
    result.drop(columns=['key_0', 'Country'], axis=1, inplace=True)

    # Save new dataset
    result.to_csv('./datasetOfficial.csv')


def format():
    # Caricamento dataset iniziale e campione da clusterizzare
    buffer = pd.read_csv("buffer.csv")
    df = pd.read_csv("datasetOfficial.csv")
    official = df.columns

    # Filtraggio delle colonne sulle quali eseguire la one hot encode
    categories = buffer['Categories']
    genres = buffer['Tags']
    developers = buffer['Developers']
    publishers = buffer['Publishers']
    countries = buffer['Country']

    # Esecuzione della one hot encode
    one_hot = MultiLabelBinarizer()

    resultCategories = pd.DataFrame(one_hot.fit_transform(categories.dropna().str.split(',')),
                                    columns=one_hot.classes_, index=buffer.index)
    resultCategories = resultCategories.add_prefix('Ctg_')

    resultGenres = pd.DataFrame(one_hot.fit_transform(genres.dropna().str.split(',')),
                                columns=one_hot.classes_, index=buffer.index)
    resultGenres = resultGenres.add_prefix('Tag_')

    resultDevelopers = pd.DataFrame(one_hot.fit_transform(developers.dropna().str.split(',')),
                                    columns=one_hot.classes_, index=buffer.index)
    resultDevelopers = resultDevelopers.add_prefix('Dvp_')

    resultPublishers = pd.DataFrame(one_hot.fit_transform(publishers.dropna().str.split(',')),
                                    columns=one_hot.classes_, index=buffer.index)
    resultPublishers = resultPublishers.add_prefix('Pbl_')

    resultCountries = pd.DataFrame(one_hot.fit_transform(countries.dropna().str.split(' ')),
                                   columns=one_hot.classes_, index=buffer.index)

    # Merge dei risultati ottenuti in un unico dataframe e rimozione delle colonne inutilizzate
    result = pd.merge(buffer, resultCategories, on=buffer.index)
    result.drop(columns=['key_0', 'Categories'], axis=1, inplace=True)

    result = pd.merge(result, resultGenres, on=buffer.index)
    result.drop(columns=['key_0', 'Tags'], axis=1, inplace=True)

    result = pd.merge(result, resultDevelopers, on=buffer.index)
    result.drop(columns=['key_0', 'Developers'], axis=1, inplace=True)

    result = pd.merge(result, resultPublishers, on=buffer.index)
    result.drop(columns=['key_0', 'Publishers'], axis=1, inplace=True)

    result = pd.merge(result, resultCountries, on=buffer.index)
    result.drop(columns=['key_0', 'Country'], axis=1, inplace=True)

    # Aggiunta delle colonne non presenti nel campione, ma nel dataset
    # Mappa per tenere traccia di eventuali nuove colonne presenti all'interno del
    #  campione, ma non nel dataset
    map = {}
    oldColumns = result.columns
    for header in official:
        if header not in oldColumns:
            result[header] = 0
        else:
            map[header] = True

    # Aggiunta di eventuali nuove colonne al dataframe e rimozione
    # di esse dal campione per permettere la clusterizzazione
    for c in oldColumns:
        if c not in map:
            result = result.drop(c, axis=1)
            df[c] = 0

    # Rimozione di eventuali colonne "Unnamed"
    df = df.filter(regex="^(?!Unnamed)", axis=1)

    # Salvataggio del dataset aggiornato in un file temporaneo
    df.to_csv("datasetTemp.csv")
    return result

def gigino():
    loaded = pickle.load(open("serializedCluster", 'rb'))
    print(loaded.labels_)
    valueToPredict = format()
    print(valueToPredict.filter(regex=("^Tag_Cook$"), axis=1))
    valueToPredict = valueToPredict.drop(['Id', 'Username', 'Tag_Action', 'Ctg_demo', 'usesMultiplayer'], axis=1)
    print(valueToPredict)
    cluster = loaded.predict(valueToPredict)
    print(cluster[0])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    gigino()
    #format()
    #main()
    #registerVote(False)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
