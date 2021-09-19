import json
import traceback

from model.algorithms import decide_init_actress_id


def lambda_handler(event, context):

    try:
        # ここから AI アルゴリズム実行
        ids = decide_init_actress_id()
        # ここまで

        return {
            'statusCode': 200,
            'body': json.dumps({"ids": ids})
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({"error": traceback.format_exc()})
        }
