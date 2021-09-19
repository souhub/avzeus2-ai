import uuid
import json
import traceback

import boto3

from model.algorithms import recommend_from_img_path

s3_client = boto3.client('s3')


def lambda_handler(event, context):
    body = event['body']

    unique_key = '{}.jpeg'.format(uuid.uuid4())
    download_path = '/tmp/{}'.format(unique_key)

    # .jpeg 以外の拡張子だとエラーが出るため
    try:
        is_face, ids = recommend_from_img_path(body, download_path)

        if not is_face:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    "is_face": is_face,
                    "ids": ids
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

        return {
            'statusCode': 200,
            'body': json.dumps({
                "is_face": is_face,
                "ids": ids,
                "key": 'https://dpgtkhmgfsuru.cloudfront.net/{}'.format(unique_key)
            })
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({"error": traceback.format_exc()})
        }

    except:
        return {
            'statusCode': 200,
            'body': json.dumps({
                "is_face": is_face,
                "ids": ids
            })
        }
