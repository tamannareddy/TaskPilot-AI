# TaskPilot/ai_parser.py
import re
from datetime import datetime, timedelta

def parse_text(user_input):
    """
    Parse messy text into structured event data.
    Returns: { "title": str, "date": "YYYY-MM-DD", "time": "HH:MM" }
    """

    title = user_input.strip().capitalize()
    date = datetime.now().strftime("%Y-%m-%d")
    time = "10:00"

    # Try to extract time like "10am" or "3:30pm"
    match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', user_input.lower())
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2)) if match.group(2) else 0
        meridian = match.group(3)
        if meridian == "pm" and hour != 12:
            hour += 12
        if meridian == "am" and hour == 12:
            hour = 0
        time = f"{hour:02d}:{minute:02d}"

    # Handle "tomorrow"
    if "tomorrow" in user_input.lower():
        date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    return {"title": title, "date": date, "time": time}
