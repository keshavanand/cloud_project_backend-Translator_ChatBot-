from chalice import Chalice
import json
from utils.translate_helper import translate_text
from utils.dynamodb_helper import save_conversation, get_conversation
from utils.lex_helper import LexHelper
from utils.polly_helper import PollyHelper
from utils.cloudwatch_helper import CloudWatchHelper
import os

app = Chalice(app_name="chalice-chatbot")

# # Load environment variables
POLLY_VOICE_ID = os.environ.get("POLLY_VOICE_ID", "Joanna")

@app.route("/chat", methods=["POST"])
def chat():
    request = app.current_request
    user_input = request.json_body.get("input")
    user_language = request.json_body.get("language", "en")

    # Translate user input to English for Lex if needed
    translated_input = (
        translate_text(user_input, user_language, "en") if user_language != "en" else user_input
    )

    lex_helper = LexHelper()
    lex_response = lex_helper.send_to_lex(translated_input)

    # Translate Lex response back to user’s language if needed
    translated_response = (
        translate_text(lex_response, "en", user_language) if user_language != "en" else lex_response
    )

    # Log to CloudWatch
    cloudwatch_helper = CloudWatchHelper(
        log_group_name="YourLogGroupName", 
        log_stream_name="YourLogStreamName"
    )
    cloudwatch_helper.log_event(f"User input: {user_input} | Translated: {translated_input}")
    cloudwatch_helper.log_event(f"Lex response: {lex_response} | Translated back: {translated_response}")

    # Save conversation in DynamoDB
    save_conversation(user_input, translated_response)

    # Convert response to audio
    polly_helper = PollyHelper()
    audio_response = polly_helper.text_to_speech(translated_response, voice_id=POLLY_VOICE_ID)

    return {"response": translated_response, "audio": str(audio_response)}
