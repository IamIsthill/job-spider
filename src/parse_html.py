from bs4 import BeautifulSoup
from typing import Any


def parseHtml(content:str):
    return BeautifulSoup(content, "html.parser")

def findContent(doc: Any, selector: dict) -> str | None:
    content = doc.find_all(attrs=selector)

    if not content: return None

    return content[0].get_text(strip=True)