from boto3 import client

class LexHelper:
    def __init__(self, bot_name, bot_alias, user_id):
        self.lex_client = client('lex-runtime')
        self.bot_name = bot_name
        self.bot_alias = bot_alias
        self.user_id = user_id

    def send_message(self, message):
        response = self.lex_client.post_text(
            botName=self.bot_name,
            botAlias=self.bot_alias,
            userId=self.user_id,
            inputText=message
        )
        return response['message'], response['intentName']

    def get_intent(self, message):
        response = self.send_message(message)
        return response[1]  # Return the intent name

    def get_response(self, message):
        response = self.send_message(message)
        return response[0]  # Return the bot's response