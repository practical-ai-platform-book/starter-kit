from asyncio import sleep
from typing import Any, Dict, Tuple
from urllib.parse import urlparse

import google.auth
from aiohttp import ClientSession, DummyCookieJar
from google.auth.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2.id_token import fetch_id_token


def prepare_authorization(credentials: Credentials, url: str) -> str:
    request = Request()
    if hasattr(credentials, "id_token"):
        # 開発者がローカルで実行する時
        # Ref: https://cloud.google.com/run/docs/authenticating/developers
        credentials.refresh(request)
        return f"Bearer {credentials.id_token}"
    # CloudRun 上でサービス間通信する時
    # https://cloud.google.com/run/docs/authenticating/service-to-service
    urlparts = urlparse(url)
    audience = f"{urlparts.scheme}://{urlparts.netloc}/"  # url without path
    id_token = fetch_id_token(request, audience)
    return f"Bearer {id_token}"


class CloudRunClient:
    def __init__(self) -> None:
        self.session = ClientSession(cookie_jar=DummyCookieJar())
        self.credentials, _ = google.auth.default()

    async def close(self) -> None:
        await self.session.close()
        # Wait 250 ms for the underlying SSL connections to close
        await sleep(0.250)

    async def get(
        self, url: str, params: Dict[str, str], need_auth: bool = False
    ) -> Tuple[int, Any]:
        if need_auth:
            authorization = prepare_authorization(self.credentials, url)
            headers = {"authorization": authorization}
        else:
            headers = {}

        async with self.session.get(url, headers=headers, params=params) as res:
            if res.status < 400:
                return res.status, await res.json()
            # エラー時はボディを使わないため None を返す
            return res.status, None
