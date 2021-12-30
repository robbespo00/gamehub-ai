from sklearn.cluster import KMeans
import pandas as pd
import pickle


df = pd.read_csv('datasetOfficial.csv')
X = df.drop(['Id', 'Username', 'Tag_Action', 'Ctg_demo', 'usesMultiplayer'], axis=1)
predictValue = pd.read_csv("buffer.csv")
predictValue = predictValue.drop(['Id', 'Username', 'Tag_Action', 'Ctg_demo', 'usesMultiplayer'], axis=1)
km = KMeans(n_clusters=5, max_iter=1000).fit(X)
cluster = km.predict(predictValue)
print(cluster)
print(km.predict(predictValue))
pickle.dump(km, open("serializedCluster", 'wb'))
loaded = pickle.load(open("serializedCluster", 'rb'))
print(loaded.predict(predictValue))
cluster_map = pd.DataFrame()
cluster_map['data_index'] = X.index.values
cluster_map['cluster'] = km.labels_
df['cluster'] = km.labels_
listMaps = []
for i in range (0, 5):
    tagsHead = df.filter(regex="((^Tag_.*$)|(usesMultiplayer))", axis=1).columns
    tagsMap = {}
    filteredDf = df.filter(regex="((^Tag_.*$)|(usesMultiplayer)|(cluster))", axis=1)
    for tag in tagsHead:
        tagColumn = filteredDf.filter(like=tag, axis=1)
        buffer = filteredDf[filteredDf[tag]==1]
        tagsMap[tag] = len(buffer[buffer['cluster']==i])
    listMaps.append(tagsMap)
print(listMaps)
couple = (km, listMaps)
pickle.dump(couple, open("serializedCouple", 'wb'))
km2 = pickle.load(open("serializedCouple", 'rb'))[0]
print(km2.predict(predictValue))


valueToPredict = pd.read_csv("buffer.csv")
valueToPredict = valueToPredict.drop(['Id', 'Username', 'Tag_Action', 'Ctg_demo', 'usesMultiplayer'], axis=1)
print(valueToPredict)
cluster = loaded.predict(valueToPredict)
print(cluster)


valueToPredict = pd.read_csv("buffer.csv")
valueToPredict = valueToPredict.drop(['Id', 'Username', 'Tag_Action', 'Ctg_demo', 'usesMultiplayer'], axis=1)
print(valueToPredict)
cluster = loaded.predict(valueToPredict)
print(cluster)