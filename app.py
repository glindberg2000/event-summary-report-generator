"""
event_summary_reporter.py

A Flask application designed to generate PDF event summary reports from JSON input.
This script allows users to input event details via a POST request and returns a PDF report
either directly or through a secure hashed link. The app is designed to be called 
from an OpenAI GPT function.

Author: glindberg2000
Date: 3/13/2024
Version: 1.0.3
"""

from flask import Flask, request, send_file, jsonify, abort, send_from_directory
import hashlib
import os
import uuid
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Define the application version
APP_VERSION = "1.0.3"

app = Flask(__name__)

# Temporary in-memory storage for hash to filename mapping.
# Note: Consider replacing with a more persistent storage solution for production use.
hash_map = {}


@app.route("/openapi.yaml")
def openapi_spec():
    return send_from_directory(".", "openapi.yaml")


@app.route("/version", methods=["GET"])
def get_version():
    """
    A route to return the current version of the application.
    """
    return jsonify(version=APP_VERSION)


@app.route("/privacy-policy")
def privacy_policy():
    return send_from_directory(
        os.path.join(app.root_path), "privacy.txt", as_attachment=True
    )


def generate_unique_filename():
    """Generates a unique filename using a UUID and timestamp to prevent filename collisions."""
    return f"report_{uuid.uuid4()}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"


def generate_hash_for_file(filename):
    """Generates a SHA-256 hash for the given filename for secure file retrieval."""
    hasher = hashlib.sha256()
    hasher.update(filename.encode("utf-8"))
    return hasher.hexdigest()


def generate_event_summary_report(input_data, filename):
    """
    Generates a PDF report based on provided input data and saves it to the given filename.

    Args:
        input_data (dict): A dictionary with specific keys detailing the event.
        filename (str): Destination filename for the generated PDF report.
    """
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    Story = []

    title = Paragraph("Event Summary Report", styles["Title"])
    Story.append(title)
    Story.append(Spacer(1, 12))

    def add_section(header, content_list):
        """
        Adds a section to the PDF document with a header and associated content paragraphs.

        Args:
            header (str): The section header.
            content_list (list): A list of strings, each representing a paragraph of content.
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
    """Endpoint to generate a PDF report based on input event details."""
    input_data = request.json.get("input_data", {})
    if not input_data:
        return jsonify(error="Missing input data"), 400

    filename = generate_unique_filename()
    generate_event_summary_report(input_data, filename)

    if request.json.get("hashed_link", False):
        file_hash = generate_hash_for_file(filename)
        hash_map[file_hash] = filename
        # Construct the full URL using request.url_root
        full_url = request.url_root.rstrip("/") + "/download-report/" + file_hash
        return jsonify(url=full_url)
    else:
        try:
            return send_file(filename, as_attachment=True)
        finally:
            if os.path.exists(filename):
                os.remove(filename)


@app.route("/download-report/<file_hash>")
def download_report(file_hash):
    """Endpoint to download a report via a secure hashed link."""
    filename = hash_map.get(file_hash)
    if filename and os.path.exists(filename):
        try:
            return send_file(filename, as_attachment=True)
        finally:
            if os.path.exists(filename):
                os.remove(filename)
    else:
        return abort(404)


if __name__ == "__main__":
    app.run(debug=True)
