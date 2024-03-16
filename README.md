# Event Summary Report Generator

## Description
The Event Summary Report Generator is a Flask application designed to generate PDF reports summarizing events based on JSON input. It processes details such as event descriptions, key participants, notable conversations, and follow-up actions, organizing them into a structured PDF document.

## Features
- Generates PDF reports from JSON input.
- Customizable report sections including event description, participants, conversations, and actions.
- Option to receive a direct download link or a secure hashed link for retrieving the generated report.
- Easy to use with any client capable of sending HTTP POST requests with JSON body.

## Installation

### Prerequisites
- Python 3.6 or later
- Pip for installing Python packages

### Setup
1. Clone the repository to your local machine.
    ```
    git clone https://github.com/glindberg2000/event-summary-report-generator.git
    ```
2. Navigate to the cloned directory.
    ```
    cd event-summary-report-generator
    ```
3. Install the required Python packages.
    ```
    pip install -r requirements.txt
    ```

## Running the Application
1. Start the Flask application.
    ```
    python app.py
    ```
2. The application will start running on `http://localhost:5000`. Use a tool like Postman or cURL to make POST requests to `http://localhost:5000/generate-report` with the appropriate JSON body.

## Usage

### Generating a Report with Direct Download
To generate a report and receive it as a direct download, send a POST request to `/generate-report` with a JSON payload as described below. The response will be a PDF file.

```json
{
  "input_data": {
    "Event Description": ["Description of the event..."],
    "Key Participants": ["List of participants..."],
    "Notable Conversations": ["Summary of conversations..."],
    "Follow-Up Actions": ["List of follow-up actions..."]
  }
}

### Generating a Report with a Secure Hashed Link (This is useful for also embedding this app into a function in OpenAI GPT. Use the openai.yaml url for scheme generation.) To generate a report and receive a secure hashed link for downloading it, include the hashed_link parameter set to true in your request payload.

{
  "input_data": {
    "Event Description": ["Description of the event..."],
    "Key Participants": ["List of participants..."],
    "Notable Conversations": ["Summary of conversations..."],
    "Follow-Up Actions": ["List of follow-up actions..."]
  },
  "hashed_link": true
}

The response will include a URL from which the report can be securely downloaded.

### Future Upgrades
Persistent Storage for Hashes: Migrate from in-memory storage to a persistent database for storing filename-hash mappings, enhancing the scalability and reliability of the hashed link feature.
Enhanced Security: Implement authentication and authorization to ensure that only authorized users can generate and access reports.

Automated Cleanup: Introduce a scheduled task or mechanism for automatically removing old reports and their corresponding hash entries to manage storage efficiently and enhance security.
Customizable PDF Templates: Allow users to define custom templates for the PDF reports, providing flexibility in how the report is formatted and what information is highlighted.
API Rate Limiting: Implement rate limiting to protect the application from abuse and ensure fair usage among all users.
License

This project is licensed under the MIT License - see the LICENSE.txt file for details.

Author: Gregory Lindberg (git:glindberg2000)