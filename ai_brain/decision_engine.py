import json

from ai_brain.investigator import IncidentInvestigator
from models.incidents import Incident
from ollama_client import generate_response
from prompts import SYSTEM_PROMPT


class AIDecisionEngine:

    def __init__(self, capabilities: list[dict]):
        self.investigator = IncidentInvestigator()
        self.capabilities = capabilities

    async def decide(self, incident: Incident) -> dict:

        evidence = self.investigator.build_evidence_context(
            incident
        )

        capabilities_text = json.dumps(
            self.capabilities,
            indent=2
        )

        prompt = f"""
{SYSTEM_PROMPT}

Available executable capabilities:

{capabilities_text}

Analyze the following incident evidence:

Evidence:
{json.dumps(evidence, indent=2, default=str)}

Important:
- You may consider any remediation idea during reasoning.
- However, the selected_action.action_id MUST exactly match one
  of the available executable capabilities.
- Do not invent an action_id.
- Selecting an action does not mean it has been executed.

Return ONLY valid JSON.
"""

        response = await generate_response(prompt)

        try:
            decision = json.loads(response)

        except json.JSONDecodeError:
            return {
                "error": "AI returned invalid JSON",
                "raw_response": response,
            }

        return decision