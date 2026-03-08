from __future__ import annotations

import random
import re
import struct
from typing import TYPE_CHECKING

from modules.minecraft.status.motd import Motd
from modules.minecraft.status.protocol.connection import Connection, UDPAsyncSocketConnection, UDPSocketConnection

if TYPE_CHECKING:
    from typing_extensions import Self


class ServerQuerier:
    MAGIC_PREFIX = bytearray.fromhex("FEFD")
    PADDING = bytearray.fromhex("00000000")
    PACKET_TYPE_CHALLENGE = 9
    PACKET_TYPE_QUERY = 0

    def __init__(self, connection: UDPSocketConnection):
        self.connection = connection
        self.challenge = 0

    @staticmethod
    def _generate_session_id() -> int:
        return random.randint(0, 2**31) & 0x0F0F0F0F

    def _create_packet(self) -> Connection:
        packet = Connection()
        packet.write(self.MAGIC_PREFIX)
        packet.write(struct.pack("!B", self.PACKET_TYPE_QUERY))
        packet.write_uint(self._generate_session_id())
        packet.write_int(self.challenge)
        packet.write(self.PADDING)
        return packet

    def _create_handshake_packet(self) -> Connection:
        packet = Connection()
        packet.write(self.MAGIC_PREFIX)
        packet.write(struct.pack("!B", self.PACKET_TYPE_CHALLENGE))
        packet.write_uint(self._generate_session_id())
        return packet

    def _read_packet(self) -> Connection:
        packet = Connection()
        packet.receive(self.connection.read(self.connection.remaining()))
        packet.read(1 + 4)
        return packet

    def handshake(self) -> None:
        self.connection.write(self._create_handshake_packet())

        packet = self._read_packet()
        self.challenge = int(packet.read_ascii())

    def read_query(self) -> QueryResponse:
        request = self._create_packet()
        self.connection.write(request)

        response = self._read_packet()
        return QueryResponse.from_connection(response)


class AsyncServerQuerier(ServerQuerier):
    def __init__(self, connection: UDPAsyncSocketConnection):
        super().__init__(connection)
        self.connection: UDPAsyncSocketConnection

    async def _read_packet(self) -> Connection:
        packet = Connection()
        packet.receive(await self.connection.read(self.connection.remaining()))
        packet.read(1 + 4)
        return packet

    async def handshake(self) -> None:
        await self.connection.write(self._create_handshake_packet())

        packet = await self._read_packet()
        self.challenge = int(packet.read_ascii())

    async def read_query(self) -> QueryResponse:
        request = self._create_packet()
        await self.connection.write(request)

        response = await self._read_packet()
        return QueryResponse.from_connection(response)


class QueryResponse:
    

    class Players:
        online: int
        max: int
        names: list[str]

        def __init__(self, online: str | int, max: str | int, names: list[str]):
            self.online = int(online)
            self.max = int(max)
            self.names = names

    class Software:
        version: str
        brand: str
        plugins: list[str]

        def __init__(self, version: str, plugins: str):
            self.version = version
            self.brand = "vanilla"
            self.plugins = []

            if plugins:
                parts = plugins.split(":", 1)
                self.brand = parts[0].strip()

                if len(parts) == 2:
                    self.plugins = [s.strip() for s in parts[1].split(";")]

    motd: Motd
    map: str
    players: Players
    software: Software

    def __init__(self, raw: dict[str, str], players: list[str]):
        try:
            self.raw = raw
            self.motd = Motd.parse(raw["hostname"], bedrock=False)
            self.map = raw["map"]
            self.players = QueryResponse.Players(raw["numplayers"], raw["maxplayers"], players)
            self.software = QueryResponse.Software(raw["version"], raw["plugins"])
        except KeyError:
            raise ValueError("The provided data is not valid")

    @classmethod
    def from_connection(cls, response: Connection) -> Self:
        response.read(len("splitnum") + 1 + 1 + 1)
        data = {}

        while True:
            key = response.read_ascii()
            if key == "hostname":
                match = re.search(
                    b"(.*?)\x00(hostip|hostport|game_id|gametype|map|maxplayers|numplayers|plugins|version)",
                    response.received,
                    flags=re.DOTALL,
                )
                motd = match.group(1) if match else ""
                data[key] = response.read(len(motd)).decode("ISO-8859-1")
                response.read(1)
            elif len(key) == 0:
                response.read(1)
                break
            else:
                value = response.read_ascii()
                data[key] = value

        response.read(len("player_") + 1 + 1)

        players = []
        while True:
            player = response.read_ascii()
            if len(player) == 0:
                break
            players.append(player)

        return cls(data, players)
