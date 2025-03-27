import boto3
import logging

class CloudWatchHelper:
    def __init__(self, log_group_name, log_stream_name):
        self.client = boto3.client('logs')
        self.log_group_name = log_group_name
        self.log_stream_name = log_stream_name
        self.create_log_group()
        self.create_log_stream()

    def create_log_group(self):
        try:
            self.client.create_log_group(logGroupName=self.log_group_name)
        except self.client.exceptions.ResourceAlreadyExistsException:
            pass

    def create_log_stream(self):
        try:
            self.client.create_log_stream(logGroupName=self.log_group_name, logStreamName=self.log_stream_name)
        except self.client.exceptions.ResourceAlreadyExistsException:
            pass

    def log_event(self, message):
        timestamp = int(round(time.time() * 1000))
        self.client.put_log_events(
            logGroupName=self.log_group_name,
            logStreamName=self.log_stream_name,
            logEvents=[
                {
                    'timestamp': timestamp,
                    'message': message
                },
            ],
        )