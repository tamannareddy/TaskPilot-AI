from flask import Flask, render_template, request, jsonify

from ai_parser import parse_text
from calendar_utils import get_calendar_service, create_event

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_event", methods=["POST"])
def add_event():

    try:
        user_input = request.json.get("note", "")

        event_data = parse_text(user_input)

        service = get_calendar_service()

        created_event = create_event(service, event_data)

        return jsonify({
            "status": "success",
            "eventLink": "https://calendar.google.com/calendar/u/0/r"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)