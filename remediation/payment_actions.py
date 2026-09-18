import httpx


SIMULATOR_URL = "http://127.0.0.1:8002"


async def recover_payment_service() -> dict:
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(
            f"{SIMULATOR_URL}/admin/recover"
        )

        response.raise_for_status()

        return response.json()