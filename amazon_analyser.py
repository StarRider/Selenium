# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 20:48:04 2018

@author: SHARON ALEXANDER
"""

from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

filename = "mobilename_link.csv"
amazon_data = pd.read_csv(filename)
numerical_data = amazon_data.loc[:,['Customers','Deal_price','Retail_price','Mobile_rating']]


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
    kmeans.fit(numerical_data)
    score_of_model.append(kmeans.score(numerical_data))
    print('.',end = "")

# ploting the elbow curve
plt.plot(n_cluster,score_of_model)
plt.xlabel('Clusters')
plt.ylabel('Score')
plt.title('The elbow curve')
plt.show()

# As per the elbow curve number of clusters = 3
num_of_cluster = 3
kmeans = KMeans(n_clusters = num_of_cluster)
kmeans.fit(numerical_data)

# Forming dataframe of cluster 
cluster_group = pd.DataFrame(data = kmeans.labels_, columns = ['Group'])
amazon_data = amazon_data.assign(Group = cluster_group)

# Saving the file
ml_data = amazon_data.iloc[:,1:]
ml_data.to_csv('mobilename_link.csv')

# deal price vs retail price
for i in range(len(ml_data)):
    grp = ml_data.iloc[i,5]
    if grp == 0:
        pattern = 'x'
        color = 'r'
    elif grp == 1:
        pattern = 'o'
        color = 'b'
    elif grp == 2:
        pattern = '*'
        color = 'g'
    plt.plot(ml_data.iloc[i,1],ml_data.iloc[i,4],color + pattern)
    
plt.xlabel('Deal price')
plt.ylabel('Retail price')
plt.title('Retail price vs Deal price with clusters')
plt.show()

# deal price vs Number of Customers
for i in range(len(ml_data)):
    grp = ml_data.iloc[i,5]
    if grp == 0:
        pattern = 'x'
        color = 'r'
    elif grp == 1:
        pattern = 'o'
        color = 'b'
    elif grp == 2:
        pattern = '*'
        color = 'g'
    plt.plot(ml_data.iloc[i,1],ml_data.iloc[i,0],color + pattern)
    
plt.xlabel('Deal price')
plt.ylabel('Number of Customers')
plt.title('Number of Customers vs Deal price with clusters')
plt.show()

# deal price vs ratings
for i in range(len(ml_data)):
    grp = ml_data.iloc[i,5]
    if grp == 0:
        pattern = 'x'
        color = 'r'
    elif grp == 1:
        pattern = 'o'
        color = 'b'
    elif grp == 2:
        pattern = '*'
        color = 'g'
    plt.plot(ml_data.iloc[i,1],ml_data.iloc[i,3],color + pattern)
    
plt.xlabel('Deal price')
plt.ylabel('Ratings of Customers')
plt.title('Ratings of Customers vs Deal price with clusters')
plt.show()

# Best choice among the clusters on the basis of number of rated customers and ratings
max0 = 0
max1 = 0
max2 = 0
maxname0 = ''
maxname1 = ''
maxname2 = ''
for i in range(len(ml_data)):
    grp = ml_data.iloc[i,5]
    rating = ml_data.iloc[i,3]
    num_of_customers = ml_data.iloc[i,0]
    compound_rating = rating*num_of_customers
    if grp == 0:
        if max0 < compound_rating:
            max0 = compound_rating
            maxname0 = i
    elif grp == 1:
        if max1 < compound_rating:
            max1 = compound_rating
            maxname1 = i
    elif grp == 2:
        if max2 < compound_rating:
            max2 = compound_rating
            maxname2 = i

print('Cluster 0s best phone:' + ml_data.iloc[maxname0,2],' Deal Price:',ml_data.iloc[maxname0,1] )
print('Cluster 1s best phone:' + ml_data.iloc[maxname1,2],' Deal Price:',ml_data.iloc[maxname1,1] )
print('Cluster 2s best phone:' + ml_data.iloc[maxname2,2],' Deal Price:',ml_data.iloc[maxname2,1] ) 

best_data = [
        ml_data.iloc[maxname0,[2,1]],
        ml_data.iloc[maxname1,[2,1]],
        ml_data.iloc[maxname2,[2,1]],
        ]
resultset = pd.DataFrame(data = best_data,
                                    index = ['Cluster 0 best','Cluster 1 best','Cluster 2 best']
                                    )




















