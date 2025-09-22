from contextlib import asynccontextmanager
from typing import AsyncIterator
import aiohttp
from aiohttp import ClientSession

@asynccontextmanager
async def create_http_client(timeout: int = 10) -> AsyncIterator[ClientSession]:
    timeout_config = aiohttp.ClientTimeout(total=timeout)
    session = aiohttp.ClientSession(timeout=timeout_config)
    try:
        yield session
    finally:
        await session.close()