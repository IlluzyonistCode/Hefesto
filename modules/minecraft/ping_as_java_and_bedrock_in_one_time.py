import asyncio
from typing import Union
from modules.minecraft.status import JavaServer, BedrockServer
from modules.minecraft.status.status_response import JavaStatusResponse, BedrockStatusResponse


async def status(server_address: str) -> Union[JavaStatusResponse, BedrockStatusResponse, None]:
    
    try:
        # Try Java Edition first
        java_server = await JavaServer.async_lookup(server_address)
        java_response = await java_server.async_status()
        return java_response
    except Exception:
        try:
            # If Java fails, try Bedrock Edition
            bedrock_server = BedrockServer.lookup(server_address)
            bedrock_response = await bedrock_server.async_status()
            return bedrock_response
        except Exception:
            # Both failed
            return None
