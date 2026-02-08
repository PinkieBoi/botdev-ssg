import re
from enum import Enum


class TextType(Enum):
    TEXT = ("", "")
    BOLD = ("b", r"**(.*?)**")
    ITALIC = ("i", r"_(.*?)_")
    CODE = ("code", r"`(.*?)`")
    LINK = (
        "a",
        re.compile(r'\[([^\]]+)\]\(\s*(?:<?([^>]+)>?)(?:\s+["\']([^"\']+)["\'])?\s*\)'),
    )
    IMAGE = (
        "img",
        re.compile(
            r'!\[([^\]]+)\]\(\s*(?:<?([^>]+)>?)(?:\s+["\']([^"\']+)["\'])?\s*\)'
        ),
    )


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        return (
            self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
