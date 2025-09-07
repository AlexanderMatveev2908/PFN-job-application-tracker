from typing import List, Optional, TypedDict, Union


class AppFile(TypedDict, total=False):
    content_type: Optional[str]
    size: float | None
    filename: Optional[str]
    buffer: Optional[bytes]
    path: Optional[str]


Primitive = str | bool
ParsedItem = Union[AppFile, Primitive]
ParsedList = List[ParsedItem]
ParsedValue = Union[ParsedItem, ParsedList]
ParsedForm = dict[str, ParsedValue]
