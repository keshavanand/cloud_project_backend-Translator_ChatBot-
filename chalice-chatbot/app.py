from chalice import Chalice
import json
from utils.lex_helper import send_to_lex
from utils.translate_helper import translate_text
from utils.polly_helper import text_to_speech
from utils.dynamodb_helper import save_conversation, get_conversation
from utils.cloudwatch_helper import log_event

app = Chalice(app_name='chalice-chatbot')

@app.route('/chat', methods=['POST'])
def chat():
    request = app.current_request
    user_input = request.json.get('input')
    user_language = request.json.get('language', 'en')

    # Translate user input to English if necessary
    if user_language != 'en':
        user_input = translate_text(user_input, user_language, 'en')

    # Send input to Lex and get response
    lex_response = send_to_lex(user_input)

    # Log the event
    log_event('User input sent to Lex', {'input': user_input, 'response': lex_response})

    # Save conversation to DynamoDB
    save_conversation(user_input, lex_response)

    # Convert Lex response to speech
    audio_response = text_to_speech(lex_response)

    return {
        'response': lex_response,
        'audio': audio_response
    }