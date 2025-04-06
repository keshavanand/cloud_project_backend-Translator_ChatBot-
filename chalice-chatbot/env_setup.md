# Environment Setup Guide

This guide explains how to set up the environment variables required for the Chalice chatbot application.

## Steps to Set Up Environment Variables

1. **Create a `.env` File**  
   Ensure the `.env` file exists in the project root directory (`backend`). Use the following template:

   ```plaintext
   AWS_ACCESS_KEY_ID=your_aws_access_key_id
   AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
   AWS_REGION=your_aws_region
   POLLY_VOICE_ID=Joanna

   CLOUDWATCH_LOG_GROUP=YourLogGroupName
   CLOUDWATCH_LOG_STREAM=YourLogStreamName
   DYNAMODB_TABLE_NAME=YourDynamoDBTableName
   LEX_BOT_NAME=YourLexBotName
   LEX_BOT_ALIAS=YourLexBotAlias
   LEX_BOT_REGION=your_aws_region
   TRANSLATE_DEFAULT_SOURCE_LANGUAGE=en
   TRANSLATE_DEFAULT_TARGET_LANGUAGE=en
   ```

2. **Install Dependencies**  
   Install the `python-dotenv` package to load environment variables from the `.env` file:

   ```bash
   pip install python-dotenv
   ```

3. **Run the Environment Setup Script**  
   Use the `setup_env.py` script to validate the environment variables:

   ```bash
   python setup_env.py
   ```

   If any required variables are missing, the script will raise an error and list the missing variables.

4. **Add `.env` to `.gitignore`**  
   Ensure the `.env` file is excluded from version control to protect sensitive information. This is already configured in the `.gitignore` file.

## Notes

- Replace placeholder values in the `.env` file with your actual AWS credentials and service configurations.
- The `setup_env.py` script ensures all required variables are loaded before running the application.

By following these steps, your environment will be correctly configured for the Chalice chatbot application.
