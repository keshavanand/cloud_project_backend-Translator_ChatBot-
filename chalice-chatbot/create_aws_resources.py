import boto3
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

def create_dynamodb_table(table_name):
    dynamodb = boto3.client('dynamodb')
    try:
        response = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'UserId', 'KeyType': 'HASH'},  # Partition key
                {'AttributeName': 'Timestamp', 'KeyType': 'RANGE'}  # Sort key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'UserId', 'AttributeType': 'S'},
                {'AttributeName': 'Timestamp', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"DynamoDB table '{table_name}' created successfully.")
    except dynamodb.exceptions.ResourceInUseException:
        print(f"DynamoDB table '{table_name}' already exists.")

def create_cloudwatch_log_group(log_group_name):
    logs = boto3.client('logs')
    try:
        logs.create_log_group(logGroupName=log_group_name)
        print(f"CloudWatch log group '{log_group_name}' created successfully.")
    except logs.exceptions.ResourceAlreadyExistsException:
        print(f"CloudWatch log group '{log_group_name}' already exists.")

def create_cloudwatch_log_stream(log_group_name, log_stream_name):
    logs = boto3.client('logs')
    try:
        logs.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
        print(f"CloudWatch log stream '{log_stream_name}' created successfully.")
    except logs.exceptions.ResourceAlreadyExistsException:
        print(f"CloudWatch log stream '{log_stream_name}' already exists.")

def create_lex_bot(bot_name, bot_alias):
    lex = boto3.client('lex-models')
    try:
        response = lex.put_bot(
            name=bot_name,
            locale='en-US',
            childDirected=False,
            intents=[
                {
                    'intentName': 'BookAirlineTicket',
                    'intentVersion': '$LATEST'
                }
            ],
            clarificationPrompt={
                'messages': [{'contentType': 'PlainText', 'content': 'Can you please repeat that?'}],
                'maxAttempts': 2
            },
            abortStatement={
                'messages': [{'contentType': 'PlainText', 'content': 'Sorry, I could not understand. Goodbye!'}]
            }
        )
        print(f"Lex bot '{bot_name}' created successfully.")
        lex.put_bot_alias(
            name=bot_alias,
            botName=bot_name,
            botVersion='$LATEST'
        )
        print(f"Lex bot alias '{bot_alias}' created successfully.")
    except Exception as e:
        print(f"Error creating Lex bot: {e}")

def test_translate_service():
    translate = boto3.client('translate')
    try:
        response = translate.translate_text(
            Text="Hello, world!",
            SourceLanguageCode="en",
            TargetLanguageCode="es"
        )
        print("Amazon Translate is working. Test translation:", response['TranslatedText'])
    except Exception as e:
        print(f"Error testing Amazon Translate: {e}")

def test_polly_service(voice_id):
    polly = boto3.client('polly')
    try:
        response = polly.synthesize_speech(
            Text="Hello, this is a test of Amazon Polly.",
            OutputFormat="mp3",
            VoiceId=voice_id
        )
        print("Amazon Polly is working. Test speech synthesized.")
    except Exception as e:
        print(f"Error testing Amazon Polly: {e}")

if __name__ == "__main__":
    # Load resource names from environment variables
    dynamodb_table_name = os.getenv("DYNAMODB_TABLE_NAME", "DefaultTableName")
    cloudwatch_log_group = os.getenv("CLOUDWATCH_LOG_GROUP", "DefaultLogGroup")
    cloudwatch_log_stream = os.getenv("CLOUDWATCH_LOG_STREAM", "DefaultLogStream")
    lex_bot_name = os.getenv("LEX_BOT_NAME", "DefaultLexBot")
    lex_bot_alias = os.getenv("LEX_BOT_ALIAS", "DefaultLexAlias")
    polly_voice_id = os.getenv("POLLY_VOICE_ID", "Joanna")

    # Create resources
    create_dynamodb_table(dynamodb_table_name)
    create_cloudwatch_log_group(cloudwatch_log_group)
    create_cloudwatch_log_stream(cloudwatch_log_group, cloudwatch_log_stream)
    create_lex_bot(lex_bot_name, lex_bot_alias)
    test_translate_service()
    test_polly_service(polly_voice_id)

    print("AWS resources setup and service tests completed.")
