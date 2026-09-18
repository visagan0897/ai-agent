import httpx


class HealthMonitor:

    async def check(self, service: str, url: str) -> dict:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)

            response.raise_for_status()

            data = response.json()

            return {
                "service": service,
                "status": data.get("status", "unknown"),
                "status_code": response.status_code,
                "failure": data.get("failure"),
            }

        except (httpx.RequestError, httpx.HTTPStatusError) as error:
            return {
                "service": service,
                "status": "unhealthy",
                "error": str(error),
            }