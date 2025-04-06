import os
import boto3
import time
import re
from botocore.exceptions import BotoCoreError, ClientError
from utils.cloudwatch_helper import CloudWatchHelper

# Initialize clients
translate = boto3.client('translate')

cloudwatch = CloudWatchHelper(
    log_group_name=os.environ.get("LOG_GROUP_NAME"),
    log_stream_name=os.environ.get("LOG_STREAM_NAME")
)

def split_sentences(text):
    """Split input text into sentences."""
    return re.split(r'(?<=[.!?])\s+|\n+', text.strip())

def translate_text(text, source_language, target_language, max_retries=3, delay=1.0):
    """Translate multi-sentence text with retries and logs."""
    if not text:
        cloudwatch.log_event("TranslateText: Empty input received.")
        return ""

    sentences = split_sentences(text)
    translated_sentences = []

    for sentence in sentences:
        if not sentence.strip():
            continue

        attempt = 0
        while attempt < max_retries:
            try:
                response = translate.translate_text(
                    Text=sentence,
                    SourceLanguageCode=source_language if source_language else 'auto',
                    TargetLanguageCode=target_language
                )
                translated = response.get("TranslatedText", "")
                translated_sentences.append(translated)
                cloudwatch.log_event(f"Translated successfully: '{sentence}' ➝ '{translated}'")
                break  # Success
            except (BotoCoreError, ClientError) as e:
                log_message = f"[Retry {attempt+1}] Failed to translate: '{sentence}' | Error: {str(e)}"
                cloudwatch.log_event(log_message)
                attempt += 1
                time.sleep(delay * attempt)

        else:
            cloudwatch.log_event(f"[Final Failure] Translation failed for sentence: '{sentence}'")
            translated_sentences.append("[Translation failed]")

    return " ".join(translated_sentences)

def detect_language(text):
    """Detect dominant language from input text."""
    try:
        response = translate.detect_dominant_language(Text=text)
        languages = response.get('Languages', [])
        if languages:
            return languages[0]['LanguageCode']
        else:
            return None
    except (BotoCoreError, ClientError) as e:
        cloudwatch.log_event(f"DetectLanguage Error: {str(e)}")
        return None
