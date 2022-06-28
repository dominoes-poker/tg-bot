from typing import Any, Dict



class Loader:
    def __init__(self) -> None:
        ...

    def __call__(self, data: Dict[Any, Any]) -> Any:
        raise NotImplementedError
