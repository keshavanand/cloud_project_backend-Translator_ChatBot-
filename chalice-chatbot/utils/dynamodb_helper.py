from boto3 import resource

dynamodb = resource('dynamodb')
table_name = 'YourDynamoDBTableName'  # Replace with your actual DynamoDB table name
table = dynamodb.Table(table_name)

def put_item(item):
    response = table.put_item(Item=item)
    return response

def get_item(key):
    response = table.get_item(Key=key)
    return response.get('Item')

def update_item(key, update_expression, expression_attribute_values):
    response = table.update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    return response

def delete_item(key):
    response = table.delete_item(Key=key)
    return response

def scan_table():
    response = table.scan()
    return response.get('Items')