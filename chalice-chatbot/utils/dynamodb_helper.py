from boto3 import resource
import uuid

DYNAMODB_TABLE = 'DYNAMODB_TABLE' 
dynamodb = resource('dynamodb')
table = dynamodb.Table(DYNAMODB_TABLE)

def put_item(item):
    return table.put_item(Item=item)

def get_item(key):
    return table.get_item(Key=key).get('Item')

def update_item(key, update_expression, expression_attribute_values):
    return table.update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )

def delete_item(key):
    return table.delete_item(Key=key)

def scan_table():
    return table.scan().get('Items')

def save_conversation(user_input, bot_response):
    item = {
        "id": str(uuid.uuid4()),
        'UserInput': user_input,
        'BotResponse': bot_response
    }
    return put_item(item)

def get_conversation(user_input):
    return get_item({'UserInput': user_input})