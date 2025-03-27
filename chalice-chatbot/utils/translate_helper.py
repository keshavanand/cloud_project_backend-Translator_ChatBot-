import boto3

def translate_text(text, target_language):
    translate = boto3.client('translate')
    response = translate.translate_text(
        Text=text,
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']

def detect_language(text):
    translate = boto3.client('translate')
    response = translate.detect_dominant_language(Text=text)
    return response['Languages'][0]['LanguageCode'] if response['Languages'] else None