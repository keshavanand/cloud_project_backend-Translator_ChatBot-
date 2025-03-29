import boto3
import time

class CloudWatchHelper:
    def __init__(self, log_group_name, log_stream_name):
        self.client = boto3.client("logs")
        self.log_group_name = log_group_name
        self.log_stream_name = log_stream_name
        self.sequence_token = None
        self._init_stream()

    def _init_stream(self):
        try:
            streams = self.client.describe_log_streams(
                logGroupName=self.log_group_name,
                logStreamNamePrefix=self.log_stream_name
            )
            if streams["logStreams"]:
                self.sequence_token = streams["logStreams"][0].get("uploadSequenceToken")
            else:
                self.client.create_log_stream(
                    logGroupName=self.log_group_name,
                    logStreamName=self.log_stream_name
                )
        except Exception as e:
            print(f"CloudWatch log stream init failed: {e}")

    def log_event(self, message):
        timestamp = int(round(time.time() * 1000))
        kwargs = {
            "logGroupName": self.log_group_name,
            "logStreamName": self.log_stream_name,
            "logEvents": [{"timestamp": timestamp, "message": message}]
        }
        if self.sequence_token:
            kwargs["sequenceToken"] = self.sequence_token

        response = self.client.put_log_events(**kwargs)
        self.sequence_token = response.get("nextSequenceToken")