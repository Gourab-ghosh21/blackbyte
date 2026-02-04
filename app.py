import os, time
from flask import Flask, request, jsonify
from ai import ai_process
from db import update_session

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

def check_api_key(req):
    key = req.headers.get("x-api-key")
    if not key:
        return False, "API key missing"
    if key != API_KEY:
        return False, "Invalid API key"
    return True, None


@app.post("/honeypot")
def honeypot():
    valid, error = check_api_key(request)
    if not valid:
        return jsonify({"status": "error", "message": error}), 401

    payload = request.json

    session_id = payload["sessionId"]
    message = payload["message"]
    history = payload["conversationHistory"]
    metadata = payload["metadata"]

    ai_result = ai_process(session_id, message, history, metadata)

    scam_detected = False
    reply = None
    extracted = None

    if ai_result.startswith("NS"):
        scam_detected = False

    elif ai_result.startswith("S:") or ai_result.startswith("M:"):
        scam_detected = True
        reply = ai_result.split(":", 1)[1].strip('"')

    elif ai_result.startswith("DS:"):
        scam_detected = True
        extracted = ai_result.split(":", 1)[1].strip('"')

    session = update_session(session_id, extracted)

    return jsonify({
        "status": "success",
        "scamDetected": scam_detected,
        "agentReply": reply,
        "engagementMetrics": {
            "totalMessagesExchanged": session["messages"],
            "durationSeconds": int(time.time() - session["start"])
        },
        "extractedIntelligence": session["extracted"],
        "agentNotes": "Autonomous AI honeypot session"
    })


if __name__ == "__main__":
    app.run(debug=True)
