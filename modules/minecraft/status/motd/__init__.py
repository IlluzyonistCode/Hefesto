from __future__ import annotations

import re
import typing as t
from dataclasses import dataclass

from modules.minecraft.status.motd.components import Formatting, MinecraftColor, ParsedMotdComponent, TranslationTag, WebColor
from modules.minecraft.status.motd.simplifies import get_unused_elements
from modules.minecraft.status.motd.transformers import AnsiTransformer, HtmlTransformer, MinecraftTransformer, PlainTransformer

if t.TYPE_CHECKING:
    from typing_extensions import Self

    from modules.minecraft.status.status_response import RawJavaResponseMotd, RawJavaResponseMotdWhenDict
else:
    RawJavaResponseMotdWhenDict = dict

__all__ = ["Motd"]

MOTD_COLORS_RE = re.compile(r"([\xA7|&][0-9A-FK-OR])", re.IGNORECASE)


@dataclass
class Motd:
    

    parsed: list[ParsedMotdComponent]
    
    raw: RawJavaResponseMotd
    
    bedrock: bool = False
    

    @classmethod
    def parse(
        cls,
        raw: RawJavaResponseMotd,
        *,
        bedrock: bool = False,
    ) -> Self:
        
        original_raw = raw.copy() if hasattr(raw, "copy") else raw
        if isinstance(raw, list):
            raw: RawJavaResponseMotdWhenDict = {"extra": raw}

        if isinstance(raw, str):
            parsed = cls._parse_as_str(raw, bedrock=bedrock)
        elif isinstance(raw, dict):
            parsed = cls._parse_as_dict(raw, bedrock=bedrock)
        else:
            raise TypeError(f"Expected list, string or dict data, got {raw.__class__!r} ({raw!r}), report this!")

        return cls(parsed, original_raw, bedrock)

    @staticmethod
    def _parse_as_str(raw: str, *, bedrock: bool = False) -> list[ParsedMotdComponent]:
        
        parsed_motd: list[ParsedMotdComponent] = []

        split_raw = MOTD_COLORS_RE.split(raw)
        for element in split_raw:
            clean_element = element.lstrip("&§").lower()
            standardized_element = element.replace("&", "§").lower()

            if standardized_element == "§g" and not bedrock:
                parsed_motd.append(element)
                continue

            if standardized_element.startswith("§"):
                try:
                    parsed_motd.append(MinecraftColor(clean_element))
                except ValueError:
                    try:
                        parsed_motd.append(Formatting(clean_element))
                    except ValueError:
                        parsed_motd.append(element)
            else:
                parsed_motd.append(element)

        return parsed_motd

    @classmethod
    def _parse_as_dict(
        cls,
        item: RawJavaResponseMotdWhenDict,
        *,
        bedrock: bool = False,
        auto_add: list[ParsedMotdComponent] | None = None,
    ) -> list[ParsedMotdComponent]:
        
        parsed_motd: list[ParsedMotdComponent] = auto_add if auto_add is not None else []

        if (color := item.get("color")) is not None:
            parsed_motd.append(cls._parse_color(color))

        for style_key, style_val in Formatting.__members__.items():
            lowered_style_key = style_key.lower()
            if item.get(lowered_style_key) is False:
                try:
                    parsed_motd.remove(style_val)
                except ValueError:
                    continue
            elif item.get(lowered_style_key) is not None:
                parsed_motd.append(style_val)

        if (text := item.get("text")) is not None:
            parsed_motd.extend(cls._parse_as_str(text, bedrock=bedrock))
        if (translate := item.get("translate")) is not None:
            parsed_motd.append(TranslationTag(translate))
        parsed_motd.append(Formatting.RESET)

        if "extra" in item:
            auto_add = list(filter(lambda e: type(e) is Formatting and e != Formatting.RESET, parsed_motd))

            for element in item["extra"]:
                parsed_motd.extend(cls._parse_as_dict(element, auto_add=auto_add.copy()))

        return parsed_motd

    @staticmethod
    def _parse_color(color: str) -> ParsedMotdComponent:
        
        try:
            return MinecraftColor[color.upper()]
        except KeyError:
            if color == "reset":
                # see https://wiki.vg/Chat#Shared_between_all_components, `color` field
                return Formatting.RESET

            try:
                return WebColor.from_hex(color)
            except ValueError:
                raise ValueError(f"Unable to parse color: {color!r}, report this!")

    def simplify(self) -> Self:
        
        parsed = self.parsed.copy()
        old_parsed: list[ParsedMotdComponent] | None = None

        while parsed != old_parsed:
            old_parsed = parsed.copy()
            unused_elements = get_unused_elements(parsed)
            parsed = [el for index, el in enumerate(parsed) if index not in unused_elements]

        return __class__(parsed, self.raw, bedrock=self.bedrock)

    def to_plain(self) -> str:
        
        return PlainTransformer().transform(self.parsed)

    def to_minecraft(self) -> str:
        
        return MinecraftTransformer().transform(self.parsed)

    def to_html(self) -> str:
        
        return HtmlTransformer(bedrock=self.bedrock).transform(self.parsed)

    def to_ansi(self) -> str:
        
        return AnsiTransformer().transform(self.parsed)
