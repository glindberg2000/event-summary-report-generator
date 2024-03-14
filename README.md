# Event Summary Report Generator

## Description
The Event Summary Report Generator is a Flask application designed to generate PDF reports summarizing events based on JSON input. It processes details such as event descriptions, key participants, notable conversations, and follow-up actions, organizing them into a structured PDF document.

## Features
- Generates PDF reports from JSON input.
- Customizable report sections including event description, participants, conversations, and actions.
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

## Example Request
To generate a report, send a POST request to `/generate-report` with a JSON payload in the following format:
```json
{
  "input_data": {
    "Event Description": ["Description of the event..."],
    "Key Participants": ["List of participants..."],
    "Notable Conversations": ["Summary of conversations..."],
    "Follow-Up Actions": ["List of follow-up actions..."]
  }
}

A PDF report will be generated and returned as a downloadable file.

License

This project is licensed under the MIT License - see the LICENSE.txt file for details.

Author: Gregory Lindberg, (GLINDBERG2000)