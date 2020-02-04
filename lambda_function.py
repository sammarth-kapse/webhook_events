import json
from pr_data import get_entities_from_webhook_data


def lambda_handler(event, context):
    response = json.loads(event["body"])
    output = get_entities_from_webhook_data(response)
    print(json.dumps(output, indent=4))
    return {
        'statusCode': 200,
        'body': "Webhook Data Sent from Lambda"
    }
