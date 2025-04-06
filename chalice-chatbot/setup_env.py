import os
from dotenv import load_dotenv

def setup_environment():
    # Load environment variables from .env file
    load_dotenv()

    # Validate required environment variables
    required_vars = [
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_REGION",
        "POLLY_VOICE_ID",
        "CLOUDWATCH_LOG_GROUP",
        "CLOUDWATCH_LOG_STREAM",
        "DYNAMODB_TABLE_NAME",
        "LEX_BOT_NAME",
        "LEX_BOT_ALIAS",
        "LEX_BOT_REGION",
        "TRANSLATE_DEFAULT_SOURCE_LANGUAGE",
        "TRANSLATE_DEFAULT_TARGET_LANGUAGE",
    ]

    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

    print("Environment variables loaded successfully.")

if __name__ == "__main__":
    setup_environment()