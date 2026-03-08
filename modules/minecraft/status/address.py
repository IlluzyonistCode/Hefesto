from __future__ import annotations

import ipaddress
import sys
import warnings
from pathlib import Path
from typing import NamedTuple, TYPE_CHECKING
from urllib.parse import urlparse

import dns.resolver

import dns

if TYPE_CHECKING:
    from typing_extensions import Self


__all__ = ("Address", "minecraft_srv_address_lookup", "async_minecraft_srv_address_lookup")


def _valid_urlparse(address: str) -> tuple[str, int | None]:
    
    tmp = urlparse("//" + address)
    if not tmp.hostname:
        raise ValueError(f"Invalid address '{address}', can't parse.")

    return tmp.hostname, tmp.port


class _AddressBase(NamedTuple):
    

    host: str
    port: int


class Address(_AddressBase):
    

    def __init__(self, *a, **kw):
        self._cached_ip: ipaddress.IPv4Address | ipaddress.IPv6Address | None = None

        self._ensure_validity(self.host, self.port)

    @staticmethod
    def _ensure_validity(host: object, port: object) -> None:
        if not isinstance(host, str):
            raise TypeError(f"Host must be a string address, got {type(host)} ({host!r})")
        if not isinstance(port, int):
            raise TypeError(f"Port must be an integer port number, got {type(port)} ({port!r})")
        if port > 65535 or port < 0:
            raise ValueError(f"Port must be within the allowed range (0-2^16), got {port!r}")

    @classmethod
    def from_tuple(cls, tup: tuple[str, int]) -> Self:
        
        return cls(host=tup[0], port=tup[1])

    @classmethod
    def from_path(cls, path: Path, *, default_port: int | None = None) -> Self:
        
        address = str(path)
        return cls.parse_address(address, default_port=default_port)

    @classmethod
    def parse_address(cls, address: str, *, default_port: int | None = None) -> Self:
        
        hostname, port = _valid_urlparse(address)
        if port is None:
            if default_port is not None:
                port = default_port
            else:
                raise ValueError(
                    f"Given address '{address}' doesn't contain port and default_port wasn't specified, can't parse."
                )
        return cls(host=hostname, port=port)

    def resolve_ip(self, lifetime: float | None = None) -> ipaddress.IPv4Address | ipaddress.IPv6Address:
        
        if self._cached_ip is not None:
            return self._cached_ip

        host = self.host
        if self.host == "localhost" and sys.platform == "darwin":
            host = "127.0.0.1"
            warnings.warn(
                "On macOS because of some mysterious reasons we can't resolve localhost into IP. "
                "Please, replace 'localhost' with '127.0.0.1' (or '::1' for IPv6) in your code to remove this warning.",
                category=RuntimeWarning,
                stacklevel=2,
            )

        try:
            ip = ipaddress.ip_address(host)
        except ValueError:
            ip_addr = dns.resolve_a_record(self.host, lifetime=lifetime)
            ip = ipaddress.ip_address(ip_addr)

        self._cached_ip = ip
        return self._cached_ip

    async def async_resolve_ip(self, lifetime: float | None = None) -> ipaddress.IPv4Address | ipaddress.IPv6Address:
        
        if self._cached_ip is not None:
            return self._cached_ip

        host = self.host
        if self.host == "localhost" and sys.platform == "darwin":
            host = "127.0.0.1"
            warnings.warn(
                "On macOS because of some mysterious reasons we can't resolve localhost into IP. "
                "Please, replace 'localhost' with '127.0.0.1' (or '::1' for IPv6) in your code to remove this warning.",
                category=RuntimeWarning,
                stacklevel=2,
            )

        try:
            ip = ipaddress.ip_address(host)
        except ValueError:
            ip_addr = await dns.async_resolve_a_record(self.host, lifetime=lifetime)
            ip = ipaddress.ip_address(ip_addr)

        self._cached_ip = ip
        return self._cached_ip


def minecraft_srv_address_lookup(
    address: str,
    *,
    default_port: int | None = None,
    lifetime: float | None = None,
) -> Address:
    
    host, port = _valid_urlparse(address)

    if port is not None:
        return Address(host, port)

    try:
        host, port = dns.resolve_mc_srv(host, lifetime=lifetime)
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        if default_port is None:
            raise ValueError(
                f"Given address '{address}' doesn't contain port, doesn't have an SRV record pointing to a port,"
                " and default_port wasn't specified, can't parse."
            )
        port = default_port

    return Address(host, port)


async def async_minecraft_srv_address_lookup(
    address: str,
    *,
    default_port: int | None = None,
    lifetime: float | None = None,
) -> Address:
    
    host, port = _valid_urlparse(address)

    if port is not None:
        return Address(host, port)

    try:
        host, port = await dns.async_resolve_mc_srv(host, lifetime=lifetime)
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        if default_port is None:
            raise ValueError(
                f"Given address '{address}' doesn't contain port, doesn't have an SRV record pointing to a port,"
                " and default_port wasn't specified, can't parse."
            )
        port = default_port

    return Address(host, port)
