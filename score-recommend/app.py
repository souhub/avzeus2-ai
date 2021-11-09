import json
import traceback
import os

import requests

from model.algorithms import recommend_from_score_dict


API_ID = os.environ.get('API_ID')
AFFIRIATE_ID = os.environ.get('AFFIRIATE_ID')
DMM_API_BASE_URL = os.environ.get('DMM_API_BASE_URL')


def lambda_handler(event, context):
    # 受け取った女優情報からAIにわたす形にデータ加工
    # body = json.loads(event['body'])
    # scores_with_id = {}

    # for actress in body['actresses']:
    #     id = actress['id']
    #     score = actress['score']
    #     scores_with_id[id] = score
    body = json.loads(event['body'])

    try:
        # ここから AI アルゴリズム実行
        # ids = recommend_from_score_dict(scores_with_id)
        ids = recommend_from_score_dict(body)
        # ここまで

        # ID配列から女優情報を取得
        actresses = []
        for id in ids:
            payload = {'api_id': API_ID,
                       'affiliate_id': AFFIRIATE_ID,
                       'actress_id': id}

            r = requests.get(
                DMM_API_BASE_URL, params=payload)

            actress = r.json()['result']['actress'][0]
            actresses.append(actress)
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS, POST'
            },
            'body': json.dumps(actresses)
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({"error": traceback.format_exc()})
        }
