import boto3

class PollyHelper:
    def __init__(self, region_name='us-east-1'):
        self.polly_client = boto3.client('polly', region_name=region_name)

    def synthesize_speech(self, text, voice_id='Joanna', output_format='mp3'):
        response = self.polly_client.synthesize_speech(
            Text=text,
            VoiceId=voice_id,
            OutputFormat=output_format
        )
        
        if 'AudioStream' in response:
            audio_stream = response['AudioStream'].read()
            return audio_stream
        else:
            raise Exception("Could not synthesize speech")

    def list_voices(self):
        response = self.polly_client.describe_voices()
        return response['Voices']