import requests
import json
import logging
from requests_toolbelt.utils import dump

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def send_report_generation_request(url, payload):
    """
    Sends a POST request to the specified URL with the given JSON payload.

    Parameters:
        url (str): The URL of the API endpoint.
        payload (dict): The JSON payload for the POST request.

    Returns:
        Response: The response object from the requests library.
    """
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        # Log basic info about the request and response
        logger.debug("URL: %s", url)
        logger.debug("Status Code: %s", response.status_code)
        logger.debug("Headers: %s", response.headers)

        # Check if the response is binary (e.g., PDF)
        if response.headers.get("Content-Type") == "application/pdf":
            logger.debug("Received a PDF file.")
            # Optionally save the PDF to a file
            with open("output.pdf", "wb") as f:
                f.write(response.content)
        else:
            # If response is not binary, it's safer to log
            logger.debug("Response: %s", response.text)

        return response
    except requests.RequestException as e:
        logger.error("An error occurred while sending the request: %s", e)
        return None


if __name__ == "__main__":
    # Define the API endpoint URL
    api_url = (
        "https://event-summary-report-generator-cryptoplato.replit.app/generate-report"
        # "http://localhost:5000/generate-report"
    )

    # Define the payload for the POST request
    payload = {
        "input_data": {
            "Event Description": [
                "A comprehensive overview of the annual tech conference focusing on the future of technology, including AI advancements, cybersecurity, and innovative startups."
            ],
            "Key Participants": [
                "Tech industry leaders, innovative startups, cybersecurity experts, and AI researchers"
            ],
            "Notable Conversations": [
                "Keynote on AI's future impact on society",
                "Panel discussion on cybersecurity challenges",
                "Startup pitch session introducing groundbreaking technologies",
            ],
            "Follow-Up Actions": [
                "Attendees encouraged to network and form collaborations",
                "Launch of a new platform for tech innovation",
                "Publication of a detailed report summarizing the conference findings",
            ],
        },
        "hashed_link": True,  # This line requests a hashed link instead of a direct PDF
    }

    # Send the POST request and get the response
    response = send_report_generation_request(api_url, payload)

    if response is not None:
        # Print the status code and response body for further debugging
        logger.info("Response Status Code: %s", response.status_code)
        logger.info("Response Body:\n%s", response.content)
    else:
        logger.error("Failed to receive a response.")
