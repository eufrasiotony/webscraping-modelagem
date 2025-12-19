
import pandas as pd
import sklearn.model_selection as ms
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, MinMaxScaler

base = pd.read_csv("basegeral.csv", delimiter=';')

base = base.dropna()

X = base.drop(columns=['flag_gol', 'awayteam', 'hometeam', 'idpartida'])
y = base['flag_gol']

scaler = MinMaxScaler().fit(X)
features_scale = scaler.transform(X)

X_train = features_scale[:1800]
X_test = features_scale[1800:2800]
testebase = base.values.tolist()[1800:2800]
y_train = y[:1800]
y_test = y[1800:2800]

classifier = LogisticRegression()
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
lista_prob.to_csv('probs-games-0.csv', index=False)

y_result_prob = np.concatenate((y_pred.reshape(len(y_pred), 1), y_pred_prob.reshape(len(y_pred_prob), 1)), 1)

cm = confusion_matrix(y_test, y_pred)




