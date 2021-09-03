import json

import pandas as pd


def lambda_handler(event, context):

    data = {"year": [2010, 2011, 2012, 2013],
            "pref": ["千葉", "山口", "岐阜", "東京"]}

    df = pd.DataFrame(data)
    print(df)

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
    # return {
    #     "statusCode": 200,
    #     "body": json.dumps({
    #         "message": "hello world",
    #         # "location": ip.text.replace("\n", "")
    #     }),
    # }
