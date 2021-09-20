import json

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

INPUTS_PATH = '/opt/ml/inputs/'
#INPUTS_PATH = '../inputs/'

def decide_init_actress_id() -> list:

    n_clusters = 5
    df = pd.read_csv(INPUTS_PATH+'actress_data.csv')
    vec = df[['elem']].values
    model = KMeans(
        n_clusters=n_clusters,
        n_init=10,
        max_iter=300,
        tol=0.01,
        random_state=int(np.random.random_sample() * 1000),
        n_jobs=2
    )
    model.fit(vec)
    center_vec = model.cluster_centers_
    ids = df['id'].tolist()
    init_actress_id = []

    for i in range(n_clusters):

        sort_list = np.argsort(np.square(vec - center_vec[i]).sum(axis=1))
        group_actresses = []
        for index in sort_list[:5]:
                
                group_actresses.append(str(ids[index]))
                
        init_actress_id.append(group_actresses)

    return init_actress_id
