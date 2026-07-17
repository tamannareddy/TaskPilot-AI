import os
import json
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def parse_text(user_input):
    today = datetime.now().strftime("%Y-%m-%d")

    prompt = f"""
You are TaskPilot AI.

Convert the user's note into ONLY valid JSON.

Today's date is {today}.

Treat THIS as the current date.
Never invent another current date.

User Input:
{user_input}

Return ONLY valid JSON.

Format:

{{
    "title": "",
    "date": "",
    "time": ""
}}

Rules:

1. If the user explicitly provides a time
   (5 pm, 5:45 pm, 17:45, 8:30 am),
   NEVER change it.

2. Preserve the exact time.

3. If no time is given, infer one using:

- morning = 09:00
- afternoon = 14:00
- evening = 18:00
- night = 21:00

4. Title Rules

- Proper capitalization.
- Expand abbreviations:
    phy → Physics
    chem → Chemistry
    maths → Mathematics
    tt → Table Tennis

5. Date Rules

Today's date is {today}.

Use THIS date for ALL calculations.

Examples:

- today → {today}
- tomorrow → one day after {today}
- next Monday → calculate from {today}

If no date is mentioned,
assume today.

Always return a FUTURE date when possible.

Never invent a random month or day.

6. Time Rules

If the user specifies only a time without AM/PM:

- If that time today is still in the future, assume today.
- If that time has already passed today, assume the next reasonable occurrence.
- Prefer PM for practice, gym, sports, meetings and classes unless AM is explicitly written.

Return:

- date as YYYY-MM-DD
- time as HH:MM (24-hour)

Return ONLY JSON.

No markdown.
No explanation.
"""

    response = model.generate_content(prompt)

    text = response.text.strip()
    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    result = json.loads(text)

    print("Gemini Output:", result)

    return result