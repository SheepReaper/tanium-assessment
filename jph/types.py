from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Union

    from model import JPHType

    OptionValue = Union[int, str, None, JPHType]


class JPHRequestOptions:
    method = ""
    resource = ""
    resource_id: Optional[int] = None
    data: Optional[JPHType] = None

    def __init__(self, **kwargs: OptionValue) -> None:
        for prop, value in [(kw, v) for (kw, v) in kwargs.items() if hasattr(self, kw)]:
            setattr(self, prop, value)
