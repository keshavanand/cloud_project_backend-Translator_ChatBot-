# Chalice Chatbot

This project is a backend application built using the Chalice framework for creating a multilingual chatbot. The chatbot leverages various AWS services to provide a seamless user experience.

## Project Structure

```
chalice-chatbot
├── .chalice
│   ├── config.json
├── app.py
├── requirements.txt
├── README.md
└── utils
    ├── lex_helper.py
    ├── translate_helper.py
    ├── polly_helper.py
    ├── dynamodb_helper.py
    └── cloudwatch_helper.py
```

## Features

- **Multilingual Support**: The chatbot can understand and respond in multiple languages using Amazon Translate.
- **Voice Interaction**: Users can interact with the chatbot using voice commands, thanks to Amazon Polly.
- **Persistent Storage**: User data and conversation history are stored in AWS DynamoDB.
- **Monitoring and Logging**: Application performance and events are monitored using AWS CloudWatch.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd chalice-chatbot
   ```

2. **Install Dependencies**:
   Ensure you have Python and pip installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AWS Credentials**:
   Make sure your AWS credentials are configured. You can set them up using the AWS CLI:
   ```bash
   aws configure
   ```

4. **Deploy the Chalice Application**:
   Deploy the application to AWS using:
   ```bash
   chalice deploy
   ```

## Usage

Once deployed, you can interact with the chatbot through the API endpoints defined in `app.py`. The chatbot will process user input, translate it if necessary, and respond using Amazon Lex.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.