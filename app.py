from flask import Flask, request, jsonify
import re
from datetime import datetime, timezone

app = Flask(__name__)

def normalize(value, key):
    value = str(value or "").strip()
    k = key.lower()

    if "email" in k:
        return value.lower()

    if "phone" in k or "mobile" in k:
        digits = re.sub(r"\D", "", value)

        if len(digits) == 11 and digits.startswith("1"):
            digits = digits[1:]

        if len(digits) == 10:
            return "+1" + digits

        return digits

    if "name" in k and "company" not in k:
        return " ".join(
            x.capitalize()
            for x in value.split()
        )

    return " ".join(value.split())

@app.get("/")
def home():
    return jsonify({
        "service": "MONEYBOT Business Data Cleaner",
        "status": "online",
        "version": "1.0",
        "endpoints": {
            "health": "GET /health",
            "clean": "POST /clean"
        }
    })

@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

@app.post("/clean")
def clean():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Send a JSON object"
        }), 400

    output = {
        k: normalize(v, k)
        for k, v in data.items()
    }

    return jsonify({
        "success": True,
        "data": output
    })
