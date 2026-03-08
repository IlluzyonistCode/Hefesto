from __future__ import annotations

from typing import cast

import dns.asyncresolver
import dns.resolver
from dns.rdatatype import RdataType
from dns.rdtypes.IN.A import A as ARecordAnswer
from dns.rdtypes.IN.SRV import SRV as SRVRecordAnswer


def resolve_a_record(hostname: str, lifetime: float | None = None) -> str:
    
    answers = dns.resolver.resolve(hostname, RdataType.A, lifetime=lifetime)
    answer = cast(ARecordAnswer, answers[0])
    ip = str(answer).rstrip(".")
    return ip


async def async_resolve_a_record(hostname: str, lifetime: float | None = None) -> str:
    
    answers = await dns.asyncresolver.resolve(hostname, RdataType.A, lifetime=lifetime)
    answer = cast(ARecordAnswer, answers[0])
    ip = str(answer).rstrip(".")
    return ip


def resolve_srv_record(query_name: str, lifetime: float | None = None) -> tuple[str, int]:
    
    answers = dns.resolver.resolve(query_name, RdataType.SRV, lifetime=lifetime)
    answer = cast(SRVRecordAnswer, answers[0])
    host = str(answer.target).rstrip(".")
    port = int(answer.port)
    return host, port


async def async_resolve_srv_record(query_name: str, lifetime: float | None = None) -> tuple[str, int]:
    
    answers = await dns.asyncresolver.resolve(query_name, RdataType.SRV, lifetime=lifetime)
    answer = cast(SRVRecordAnswer, answers[0])
    host = str(answer.target).rstrip(".")
    port = int(answer.port)
    return host, port


def resolve_mc_srv(hostname: str, lifetime: float | None = None) -> tuple[str, int]:
    
    return resolve_srv_record("_minecraft._tcp." + hostname, lifetime=lifetime)


async def async_resolve_mc_srv(hostname: str, lifetime: float | None = None) -> tuple[str, int]:
    
    return await async_resolve_srv_record("_minecraft._tcp." + hostname, lifetime=lifetime)
