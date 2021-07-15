from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Union

    OptionValue = Union[int, str, None]


class Post:
    userId: Optional[int] = None
    id: Optional[int] = None
    title: Optional[str] = None
    body: Optional[str] = None

    def __init__(self, **kwargs: OptionValue) -> None:
        for prop, value in [(kw, v) for (kw, v) in kwargs.items() if hasattr(self, kw)]:
            setattr(self, prop, value)


# We only have one JPH Type in use, so we use an alias
JPHType = Post
# But use this instead when there are more
# JPHType = TypeVar("JPHType", Post, ...)
# Or Union, Unions are good too...
