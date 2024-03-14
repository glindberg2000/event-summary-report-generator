"""
event_summary_reporter.py

A Flask application designed to generate PDF event summary reports from JSON input.
This script allows users to input event details via a POST request and returns a PDF report.

Author: [Your Name or GitHub Handle]
Date: [Date of Creation]
"""

from flask import Flask, request, send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

app = Flask(__name__)


def generate_event_summary_report(input_data, filename):
    """
    Generates an enhanced event summary report as a PDF file based on the provided input data.

    Parameters:
        input_data (dict): A structured dictionary containing keys and list of strings for each section of the report.
                           Expected keys: 'Event Description', 'Key Participants',
                           'Notable Conversations', 'Follow-Up Actions'.
        filename (str): The filename for the generated PDF report.

    Returns:
        None: Generates a PDF file at the specified path.
    """
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    Story = []

    # Adding the report title
    title = Paragraph("Enhanced Event Summary Report", styles["Title"])
    Story.append(title)
    Story.append(Spacer(1, 12))

    def add_section(header, content_list):
        """
        Adds a new section to the PDF report with a header and content.

        Parameters:
            header (str): The header or title of the section.
            content_list (list of str): The content of the section in a list where each item represents a paragraph.

        Returns:
            None: Modifies the Story list in place by appending content.
        """
        header_style = styles["Heading2"]
        text_style = styles["BodyText"]

        Story.append(Paragraph(header, header_style))
        for content in content_list:
            p = Paragraph(content, text_style)
            Story.append(p)
            Story.append(Spacer(1, 12))

    for section, content in input_data.items():
        add_section(section, content)

    doc.build(Story)


@app.route("/generate-report", methods=["POST"])
def generate_report():
    """
    Flask route to accept POST requests with event details in JSON format and generate a PDF report.

    Returns:
        File: The generated PDF report as a file download.
    """
    input_data = request.json.get("input_data", {})
    if not input_data:
        return {"error": "Missing input data"}, 400

    filename = "event_summary_report.pdf"
    generate_event_summary_report(input_data, filename)

    if os.path.exists(filename):
        return send_file(filename, as_attachment=True)
    else:
        return {"error": "Failed to generate the report"}, 500


if __name__ == "__main__":
    app.run(debug=True)
