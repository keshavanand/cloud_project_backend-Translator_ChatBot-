import boto3
import uuid
import os

class LexHelper:
    def __init__(self):
        self.lex_client = boto3.client('lexv2-runtime')
        self.bot_id = os.environ.get("LEX_BOT_ID")         # Set this in your environment or config
        self.bot_alias_id = os.environ.get("LEX_BOT_ALIAS_ID")
        self.locale_id = "en_US"                            # Or get from env if dynamic

    def send_message(self, message):
        response = self.lex_client.recognize_text(
            botId=self.bot_id,
            botAliasId=self.bot_alias_id,
            localeId=self.locale_id,
            sessionId=str(uuid.uuid4()),  # unique for each session
            text=message
        )
        return response

    def get_intent(self, message):
        response = self.send_message(message)
        return response.get("interpretations", [{}])[0].get("intent", {}).get("name", "")

    def get_response(self, message):
        response = self.send_message(message)
        if "messages" in response and response["messages"]:
            return response["messages"][0]["content"]
        return "No response from Lex."

    def send_to_lex(self, message):
        return self.get_response(message)