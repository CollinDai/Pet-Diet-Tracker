from flask import Flask, render_template_string
from src.services.event_history_service import EventHistoryService

app = Flask(__name__)
event_history_service = EventHistoryService()

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-g">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Pet Food Consumption Events</title>
    <style>
        body { font-family: sans-serif; background-color: #f8f9fa; }
        .container { margin: 2rem auto; max-width: 800px; }
        h1 { text-align: center; color: #343a40; }
        table { width: 100%; border-collapse: collapse; background-color: #fff; }
        th, td { padding: 0.75rem; text-align: left; border-bottom: 1px solid #dee2e6; }
        th { background-color: #e9ecef; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Event History</h1>
        <table>
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>Event</th>
                </tr>
            </thead>
            <tbody>
                {% for event in events %}
                <tr>
                    <td>{{ event.timestamp }}</td>
                    <td>{{ event.event }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    """Serves a web page with the history of detected events."""
    events = event_history_service.get_events()
    return render_template_string(HTML_TEMPLATE, events=events)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
