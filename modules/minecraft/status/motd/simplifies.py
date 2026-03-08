from __future__ import annotations

from collections.abc import Sequence

from modules.minecraft.status.motd.components import Formatting, MinecraftColor, ParsedMotdComponent, WebColor


def get_unused_elements(parsed: Sequence[ParsedMotdComponent]) -> set[int]:
    
    to_remove: set[int] = set()

    for simplifier in [get_double_items, get_double_colors, get_formatting_before_color, get_empty_text, get_end_non_text]:
        to_remove.update(simplifier(parsed))

    return to_remove


def get_double_items(parsed: Sequence[ParsedMotdComponent]) -> set[int]:
    
    to_remove: set[int] = set()

    for index, item in enumerate(parsed):
        try:
            next_item = parsed[index + 1]
        except IndexError:
            break

        if isinstance(item, (Formatting, MinecraftColor, WebColor)) and item == next_item:
            to_remove.add(index)

    return to_remove


def get_double_colors(parsed: Sequence[ParsedMotdComponent]) -> set[int]:
    
    to_remove: set[int] = set()

    prev_color: int | None = None
    for index, item in enumerate(parsed):
        if isinstance(item, (MinecraftColor, WebColor)):
            if prev_color is not None:
                to_remove.add(prev_color)
            prev_color = index

        if isinstance(item, str):
            prev_color = None

    return to_remove


def get_formatting_before_color(parsed: Sequence[ParsedMotdComponent]) -> set[int]:
    
    to_remove: set[int] = set()

    collected_formattings = []
    for index, item in enumerate(parsed):
        if isinstance(item, Formatting):
            collected_formattings.append(index)

        if len(collected_formattings) == 0:
            continue

        if isinstance(item, str):
            collected_formattings = []
            continue

        if isinstance(item, (MinecraftColor, WebColor)):
            to_remove.update(collected_formattings)
            collected_formattings = []
    return to_remove


def get_empty_text(parsed: Sequence[ParsedMotdComponent]) -> set[int]:
    
    to_remove: set[int] = set()

    for index, item in enumerate(parsed):
        if isinstance(item, str) and len(item) == 0:
            to_remove.add(index)

    return to_remove


def get_end_non_text(parsed: Sequence[ParsedMotdComponent]) -> set[int]:
    
    to_remove: set[int] = set()

    for rev_index, item in enumerate(reversed(parsed)):
        if isinstance(item, str):
            break

        if isinstance(item, (MinecraftColor, WebColor, Formatting)):
            index = len(parsed) - 1 - rev_index
            to_remove.add(index)

    return to_remove
