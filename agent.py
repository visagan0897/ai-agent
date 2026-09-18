import json

from models.requests import IncidentRequest
from ollama_client import generate_response
from prompts import SYSTEM_PROMPT


class IncidentAgent:

    async def analyze(self, incident: IncidentRequest):
        incident_data = incident.model_dump_json()

        prompt = f"""{SYSTEM_PROMPT}

Incident data:
{incident_data}
"""

        response = await generate_response(prompt)

        try:
            return json.loads(response)

        except json.JSONDecodeError:
            return {
                "error": "AI returned invalid JSON",
                "raw_response": response
            }