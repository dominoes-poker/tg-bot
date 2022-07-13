import json
from pathlib import Path
from typing import Tuple, Any, Dict

from string import Formatter


class MessagesProvider:
    def __init__(self, file_path: Path):
        with file_path.open() as messages_file:
            self._messages = json.load(messages_file)

    def __getattr__(self, attribute: str) -> str:
        if attribute not in self._messages:
            raise AttributeError(f'The message for "{attribute}" is not define')
        return self._messages[attribute]


class MessageService:
    def __init__(self, message_provider: MessagesProvider):
        self._message_provider = message_provider

    def __getattr__(self, attribute: str) -> str:
        return self._message_provider.__getattr__(attribute)

    def params(self, message_name: str) -> Tuple[str]:
        message = self._message_provider.__getattr__(message_name)
        return tuple(name for _, name, _, _ in Formatter().parse(message) if name is not None)

    def get_formatted_message(self, message_name: str, **parameters: Dict[str, Any]) -> str:
        raw_message = self._message_provider.__getattr__(message_name)
        expected_params = set(self.params(message_name))
        actual_params = set(parameters.keys())
        if expected_params != actual_params:
            raise AssertionError(
                f'Cannot format the message. Expected params: {expected_params}, actual params: {actual_params}'
            )
        return raw_message.format(**parameters)
