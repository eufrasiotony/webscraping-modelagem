
import pandas as pd
import sklearn.model_selection as ms
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.feature_selection import SelectKBest

base = pd.read_csv("basegeral.csv", delimiter=';')
base['flag_gol_1'] = 0
for ind in base.index:
    print(base['flag_gol_1'][ind])
    if base['gols'][ind] > 1:
        print(base['flag_gol_1'])
        base['flag_gol_1'][ind] = 1



base = base.dropna()

X = base.drop(columns=['flag_gol', 'scorehome', 'scoreaway', 'gols', 'flag_gol_1', 'awayteam', 'hometeam', 'idpartida'])
y = base['flag_gol_1']

scaler = MinMaxScaler().fit(X)
features_scale = scaler.transform(X)

k_best_features = SelectKBest(k='all')
k_best_features.fit_transform(X, y)
k_best_features_scores = k_best_features.scores_
raw_pairs = zip(X[1:], k_best_features_scores)
ordered_pairs = list(reversed(sorted(raw_pairs, key=lambda x: x[1])))

k_best_features_final = dict(ordered_pairs[:15])
best_features = k_best_features_final.keys()
print('')
print("Melhores features:")
print(k_best_features_final)


X_train = features_scale[:2000]
X_test = features_scale[2000:3435]
testebase = base.values.tolist()[2000:3435]
y_train = y[:2000]
y_test = y[2000:3435]



classifier = LogisticRegression()
print(y_train, X_train)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
y_pred_prob = classifier.predict_proba(X_test)
y_pred_prob = y_pred_prob[:, 1]

lista_prob = []
for index, prob in enumerate(y_pred_prob):
    probs = {
              'homeid': testebase[index][0],
              'awayid': testebase[index][3],
              'probabilidade': prob
    }
    lista_prob.append(probs)

lista_prob = pd.DataFrame(lista_prob)
lista_prob.to_csv('probs-games-1.csv', index=False)

y_result_prob = np.concatenate((y_pred.reshape(len(y_pred), 1), y_pred_prob.reshape(len(y_pred_prob), 1)), 1)

cm = confusion_matrix(y_test, y_pred)




