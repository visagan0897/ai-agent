import httpx


class LogMonitor:

    async def collect(self, service: str, url: str) -> dict:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)

            response.raise_for_status()

            data = response.json()

            return {
                "service": service,
                "logs": data.get("logs", []),
            }

        except (httpx.RequestError, httpx.HTTPStatusError) as error:
            return {
                "service": service,
                "logs": [],
                "error": str(error),
            }