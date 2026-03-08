from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from modules.minecraft.status.address import Address, async_minecraft_srv_address_lookup, minecraft_srv_address_lookup
from modules.minecraft.status.bedrock_status import BedrockServerStatus
from modules.minecraft.status.pinger import AsyncServerPinger, ServerPinger
from modules.minecraft.status.protocol.connection import (
    TCPAsyncSocketConnection,
    TCPSocketConnection,
    UDPAsyncSocketConnection,
    UDPSocketConnection,
)
from modules.minecraft.status.querier import AsyncServerQuerier, QueryResponse, ServerQuerier
from modules.minecraft.status.status_response import BedrockStatusResponse, JavaStatusResponse
from modules.minecraft.status.utils import retry

if TYPE_CHECKING:
    from typing_extensions import Self


__all__ = ["MCServer", "JavaServer", "BedrockServer"]


class MCServer(ABC):
    

    DEFAULT_PORT: int

    def __init__(self, host: str, port: int | None = None, timeout: float = 3):
        
        if port is None:
            port = self.DEFAULT_PORT
        self.address = Address(host, port)
        self.timeout = timeout

    @classmethod
    def lookup(cls, address: str, timeout: float = 3) -> Self:
        
        addr = Address.parse_address(address, default_port=cls.DEFAULT_PORT)
        return cls(addr.host, addr.port, timeout=timeout)


class JavaServer(MCServer):
    

    DEFAULT_PORT = 25565

    @classmethod
    def lookup(cls, address: str, timeout: float = 3) -> Self:
        
        addr = minecraft_srv_address_lookup(address, default_port=cls.DEFAULT_PORT, lifetime=timeout)
        return cls(addr.host, addr.port, timeout=timeout)

    @classmethod
    async def async_lookup(cls, address: str, timeout: float = 3) -> Self:
        
        addr = await async_minecraft_srv_address_lookup(address, default_port=cls.DEFAULT_PORT, lifetime=timeout)
        return cls(addr.host, addr.port, timeout=timeout)

    def ping(self, **kwargs) -> float:
        

        with TCPSocketConnection(self.address, self.timeout) as connection:
            return self._retry_ping(connection, **kwargs)

    @retry(tries=3)
    def _retry_ping(self, connection: TCPSocketConnection, **kwargs) -> float:
        pinger = ServerPinger(connection, address=self.address, **kwargs)
        pinger.handshake()
        return pinger.test_ping()

    async def async_ping(self, **kwargs) -> float:
        

        async with TCPAsyncSocketConnection(self.address, self.timeout) as connection:
            return await self._retry_async_ping(connection, **kwargs)

    @retry(tries=3)
    async def _retry_async_ping(self, connection: TCPAsyncSocketConnection, **kwargs) -> float:
        pinger = AsyncServerPinger(connection, address=self.address, **kwargs)
        pinger.handshake()
        ping = await pinger.test_ping()
        return ping

    def status(self, **kwargs) -> JavaStatusResponse:
        

        with TCPSocketConnection(self.address, self.timeout) as connection:
            return self._retry_status(connection, **kwargs)

    @retry(tries=3)
    def _retry_status(self, connection: TCPSocketConnection, **kwargs) -> JavaStatusResponse:
        pinger = ServerPinger(connection, address=self.address, **kwargs)
        pinger.handshake()
        result = pinger.read_status()
        return result

    async def async_status(self, **kwargs) -> JavaStatusResponse:
        

        async with TCPAsyncSocketConnection(self.address, self.timeout) as connection:
            return await self._retry_async_status(connection, **kwargs)

    @retry(tries=3)
    async def _retry_async_status(self, connection: TCPAsyncSocketConnection, **kwargs) -> JavaStatusResponse:
        pinger = AsyncServerPinger(connection, address=self.address, **kwargs)
        pinger.handshake()
        result = await pinger.read_status()
        return result

    def query(self) -> QueryResponse:
        
        ip = str(self.address.resolve_ip())
        return self._retry_query(Address(ip, self.address.port))

    @retry(tries=3)
    def _retry_query(self, addr: Address) -> QueryResponse:
        with UDPSocketConnection(addr, self.timeout) as connection:
            querier = ServerQuerier(connection)
            querier.handshake()
            return querier.read_query()

    async def async_query(self) -> QueryResponse:
        
        ip = str(await self.address.async_resolve_ip())
        return await self._retry_async_query(Address(ip, self.address.port))

    @retry(tries=3)
    async def _retry_async_query(self, address: Address) -> QueryResponse:
        async with UDPAsyncSocketConnection(address, self.timeout) as connection:
            querier = AsyncServerQuerier(connection)
            await querier.handshake()
            return await querier.read_query()


class BedrockServer(MCServer):
    

    DEFAULT_PORT = 19132

    @retry(tries=3)
    def status(self, **kwargs) -> BedrockStatusResponse:
        
        return BedrockServerStatus(self.address, self.timeout, **kwargs).read_status()

    @retry(tries=3)
    async def async_status(self, **kwargs) -> BedrockStatusResponse:
        
        return await BedrockServerStatus(self.address, self.timeout, **kwargs).read_status_async()
