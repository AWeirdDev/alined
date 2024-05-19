from typing import Mapping
import httpx
from .rate_limiting import apply_rate_limit


@apply_rate_limit(requests=2000, per_seconds=1)
async def send_reply_message(body: dict, headers: Mapping[str, str]) -> dict:
    """Send reply message.

    Args:
        body (dict): Body.
        headers (Mapping[str, str]): Headers.
    """
    client = httpx.AsyncClient()
    r = await client.post(
        "https://api.line.me/v2/bot/message/reply", headers=headers, json=body
    )
    r.raise_for_status()
    return r.json()
