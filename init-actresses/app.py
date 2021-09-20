import json
import traceback
import os

import requests

from model.algorithms import decide_init_actress_id


API_ID = os.environ.get('API_ID')
AFFIRIATE_ID = os.environ.get('AFFIRIATE_ID')
DMM_API_BASE_URL = os.environ.get('DMM_API_BASE_URL')


def lambda_handler(event, context):

    try:
        # ここから AI アルゴリズム実行
        groups = decide_init_actress_id()
        # ここまで

        actresses = []

        for ids in groups:
            for id in ids:
                payload = {'api_id': API_ID,
                           'affiliate_id': AFFIRIATE_ID,
                           'actress_id': id}

                r = requests.get(
                    DMM_API_BASE_URL, params=payload)

                actress = r.json()['result']['actress'][0]

                try:
                    # imageURLがない女優は消去
                    actress['imageURL']

                    # null または "" があれば代入
                    for k in actress:
                        if actress[k] == "" or actress[k] is None:
                            actress[k] = '♡♡秘密♡♡'

                    actresses.append(actress)
                    break
                except:
                    continue

        return {
            'statusCode': 200,
            'body': json.dumps({"actresses": actresses})
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({"error": traceback.format_exc()})
        }
