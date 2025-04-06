from chalice import Chalice
import json
from utils.translate_helper import translate_text, detect_language
from utils.dynamodb_helper import save_conversation, get_conversation
from utils.lex_helper import LexHelper
from utils.polly_helper import PollyHelper
from utils.cloudwatch_helper import CloudWatchHelper
import os
import base64

app = Chalice(app_name="chalice-chatbot")

# Load environment variables
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
LEX_BOT_NAME = os.environ.get("LEX_BOT_NAME", "TranslatorLingoBot")
LEX_BOT_ALIAS = os.environ.get("LEX_BOT_ALIAS", "TestBotAlias")
POLLY_VOICE_ID = os.environ.get("POLLY_VOICE_ID", "Joanna")
DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE", "DYNAMODB_TABLE")
LOG_GROUP_NAME = os.environ.get("LOG_GROUP_NAME", "TranslatorChatBotLogs")
LOG_STREAM_NAME = os.environ.get("LOG_STREAM_NAME", "ChatEventsStream")

@app.route("/chat", methods=["POST"], cors=True)
def chat():
    request = app.current_request
    user_input = request.json_body.get("input")
    user_language = request.json_body.get("language")

    # If user language not provided, detect it
    if not user_language:
        user_language = detect_language(user_input) or "en"

    # Translate user input to English for Lex if needed
    if user_language.lower() != "en":
        translated_input = translate_text(user_input, user_language, "en")
    else:
        translated_input = user_input

    # Send input to Lex
    lex_helper = LexHelper()
    lex_response = lex_helper.send_to_lex(translated_input)

    # Translate Lex response back to user’s language if needed
    if user_language.lower() != "en":
        translated_response = translate_text(lex_response, "en", user_language)
    else:
        translated_response = lex_response

    # Log events to CloudWatch
    cloudwatch_helper = CloudWatchHelper(
        log_group_name=LOG_GROUP_NAME,
        log_stream_name=LOG_STREAM_NAME
    )
    cloudwatch_helper.log_event(f"User language: {user_language} | Input: {user_input} | Translated to EN: {translated_input}")
    cloudwatch_helper.log_event(f"Lex raw response: {lex_response} | Translated back to {user_language}: {translated_response}")

    # Save conversation to DynamoDB
    save_conversation(user_input, translated_response)

    # Convert response to audio
    polly_helper = PollyHelper()
    audio_response = polly_helper.text_to_speech(translated_response, voice_id=POLLY_VOICE_ID)

    # Encode audio as base64
    audio_b64 = base64.b64encode(audio_response).decode("utf-8")

    return {
        "response": translated_response,
        "audio": f"data:audio/mp3;base64,{audio_b64}"
    }
