import json

import httpx

from config import OLLAMA_URL, OLLAMA_MODEL


async def generate_response(prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": True,
        "think": False,
        "temperature": 0.2,
        "num_predict": 500
    }

    output = []

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST",
            f"{OLLAMA_URL}/api/generate",
            json=payload
        ) as response:

            response.raise_for_status()

            async for line in response.aiter_lines():
                if not line:
                    continue

                data = json.loads(line)

                if "response" in data:
                    output.append(data["response"])

                if data.get("done"):
                    break

    return "".join(output)