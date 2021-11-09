import uuid
import json
import traceback
import os

import boto3
import requests
from model.algorithms import recommend_from_img_path

API_ID = os.environ.get('API_ID')
AFFIRIATE_ID = os.environ.get('AFFIRIATE_ID')
DMM_API_BASE_URL = os.environ.get('DMM_API_BASE_URL')

s3_client = boto3.client('s3')

headers = {
    'Access-Control-Allow-Headers': 'Content-Type, X-Requested-With',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS, POST',
}


def lambda_handler(event, context):
    body = event['body']

    unique_key = '{}.jpeg'.format(uuid.uuid4())
    download_path = '/tmp/{}'.format(unique_key)
    actresses = []

    # .jpeg 以外の拡張子だとエラーが出るため
    try:
        is_face, ids = recommend_from_img_path(body, download_path)
        if not is_face:
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    "actresses": actresses,
                    "key": ''
                })
            }

        # content-type ヘッダーを使用しないとAPI経由で保存したファイルは全部バイナリファイル扱いになってアクセスしてもすべてダウンロードされてしまい表示できない
        content_type = "image/jpeg"
        bucket = 'souhub-s3-test-function2-resized'

        payload = open(download_path, 'rb')

        s3_client.put_object(
            Body=payload,
            Bucket=bucket,
            Key=unique_key,
            ContentType=content_type)

        # ID配列から女優情報を取得

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
            'headers': headers,
            'body': json.dumps({
                "actresses": actresses,
                "key": 'https://dpgtkhmgfsuru.cloudfront.net/{}'.format(unique_key)
            })
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({"error": traceback.format_exc()})
        }
