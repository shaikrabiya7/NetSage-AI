from flask import Flask, jsonify, request, send_from_directory
import os
import csv

from rule_checker import check_network
from evidence_engine import extract_evidence


app = Flask(__name__)


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_FILE = os.path.join(
    BASE_DIR,
    "data",
    "cases.csv"
)


# -----------------------------
# Home Page
# -----------------------------

@app.route("/")
def home():

    return send_from_directory(
        os.path.join(BASE_DIR, "dashboard"),
        "index.html"
    )


# -----------------------------
# Test
# -----------------------------

@app.route("/test")
def test():

    return jsonify({
        "status": "success",
        "message": "NetSage AI backend is working"
    })


# -----------------------------
# Get All Cases
# -----------------------------

@app.route("/cases")
def cases():

    case_list = []

    with open(
        DATA_FILE,
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            case_list.append(row)

    return jsonify(case_list)


# -----------------------------
# Diagnose
# -----------------------------

@app.route("/diagnose", methods=["POST"])
def diagnose():

    case = request.get_json()

    if not case:

        return jsonify({
            "error": "No network case received"
        }), 400


    raw_evidence = case.get(
        "show_outputs",
        ""
    )


    extracted_evidence = extract_evidence(
        raw_evidence
    )


    findings = check_network(case)


    return jsonify({

        "case_id":
        case.get("case_id", "CUSTOM"),

        "symptom":
        case.get("symptom", ""),

        "extracted_evidence":
        extracted_evidence,

        "rule_checker":
        findings

    })

# -----------------------------
# Save Human Review
# -----------------------------

@app.route("/review", methods=["POST"])
def review():

    review_data = request.get_json()

    if not review_data:

        return jsonify({
            "error": "No review data received"
        }), 400


    log_file = os.path.join(
        BASE_DIR,
        "logs",
        "review_log.csv"
    )


    file_exists = os.path.exists(log_file)


    with open(
        log_file,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        fieldnames = [
            "case_id",
            "decision",
            "corrected_diagnosis",
            "comment"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )


        if not file_exists:
            writer.writeheader()


        writer.writerow({

            "case_id":
            review_data.get(
                "case_id",
                "CUSTOM"
            ),

            "decision":
            review_data.get(
                "decision",
                ""
            ),

            "corrected_diagnosis":
            review_data.get(
                "corrected_diagnosis",
                ""
            ),

            "comment":
            review_data.get(
                "comment",
                ""
            )

        })


    return jsonify({

        "status": "success",

        "message":
        "Review saved successfully"

    })
# -----------------------------
# Start Server
# -----------------------------

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )