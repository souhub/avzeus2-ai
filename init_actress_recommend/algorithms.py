import json

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

def decide_init_actress_id() -> list:

    n_clusters = 5
    df = pd.read_csv('input/actress_data.csv')
    vec = df[['elem']].values
    model = KMeans(
            n_clusters = n_clusters,
            n_init = 10,
            max_iter = 300,
            tol = 0.01,
            random_state = int(np.random.random_sample() * 1000),
            n_jobs = 2
            )
    model.fit(vec)
    center_vec = model.cluster_centers_
    ids = df['id'].tolist()
    init_actress_id = []

    for i in range(n_clusters):

        index = np.argmin(np.square(vec - center_vec[i]).sum(axis = 1))
        init_actress_id.append(str(ids[index]))
        
    return init_actress_id


def lambda_handler(event, context):

    # ここから AI アルゴリズム実行
    ids=decide_init_actress_id()
    # ここまで

    return {
        'statusCode': 200,
        'body': json.dumps({"ids":ids})
    }
