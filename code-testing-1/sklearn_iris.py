# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.linear_model import Perceptron

iris = load_iris()
X = iris.data[:, (2, 3)] # petal length, petal width 
y = (iris.target == 0).astype(int) # Iris setosa?

per_clf = Perceptron()
per_clf.fit(X, y)


len_pred = 1.5
wid_pred = 0.25
y_pred = per_clf.predict([[len_pred, wid_pred]])

print(y_pred)

petal_len = iris.data[:, (2)]
petal_wid = iris.data[:, (3)]
z = iris.target

plt.figure(dpi=1200)
plt.scatter(petal_len, petal_wid, c=z)
plt.scatter(len_pred, wid_pred, c=y_pred, marker="*")



