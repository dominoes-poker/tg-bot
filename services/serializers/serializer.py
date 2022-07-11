from typing import Any, Dict



class Serializer:
    def __init__(self) -> None:
        ...

    def __call__(self, data: Any) -> Any:
        raise NotImplementedError
