from pathlib import Path
from typing import Union

from bot.messages.service import MessageService, MessagesProvider


def create_message_service(messages_config_file_name: Union[str, Path], messages_folder_path: Path) -> MessageService:
    file_full_path = messages_folder_path / f'{messages_config_file_name}.json'
    messages_provider = MessagesProvider(file_full_path)
    return MessageService(messages_provider)
