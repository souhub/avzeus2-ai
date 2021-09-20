import json
import traceback

from model.algorithms import recommend_from_score_dict


def lambda_handler(event, context):
    body = json.loads(event['body'])

    try:
        # ここから AI アルゴリズム実行
        ids = recommend_from_score_dict(body)
        # ここまで

        return {
            'statusCode': 200,
            'body': json.dumps({"ids": ids})
            # 'body': json.dumps({"ids": ids})
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({"error": traceback.format_exc()})
        }
