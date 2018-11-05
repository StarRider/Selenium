# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 20:48:04 2018

@author: SHALOM ALEXANDER
"""

from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

filename = "mobilename_link.csv"
amazon_data = pd.read_csv(filename)

price_part = amazon_data.loc[:,['Deal_price','Retail_price']]

# plot of Retail price vs Deal price
plt.plot(price_part.loc[:,['Deal_price']],price_part.loc[:,['Retail_price']],'x')
plt.xlabel('Deal price')
plt.ylabel('Retail price')
plt.title('Retail price vs Deal price')
plt.show()


# chosen parameter
score_of_model = []
n_cluster = np.arange(1,10) # chosen after looking at the plot w.r.t deal and retail price 
print('KMeans Model...')
for clusters in n_cluster:
    kmeans = KMeans(n_clusters = clusters)
    kmeans.fit(price_part)
    score_of_model.append(kmeans.score(price_part))
    print('.',end = "")

# ploting the elbow curve
plt.plot(n_cluster,score_of_model)
plt.xlabel('Clusters')
plt.ylabel('Score')
plt.title('The elbow curve')
plt.show()







