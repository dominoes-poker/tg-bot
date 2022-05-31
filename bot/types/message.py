from aiogram.types import TelegramObject, Message, Chat

class IncommingMessage:
    def __init__(self, tg_object: TelegramObject) -> None:
        self._tg_object = tg_object

    @property
    def text(self) -> str:
        raise NotImplementedError

    @property
    def chat(self) -> Chat:
        raise NotImplementedError

    @property
    def user_id(self) -> int:
        raise NotImplementedError

class IncommingMessageWrapper(IncommingMessage):
    def __init__(self, tg_object: Message) -> None:
        super().__init__(tg_object)

    @property
    def text(self) -> str:
        return self._tg_object.text

    @property
    def chat(self) -> Chat:
        return self._tg_object.chat
    @property
    def user_id(self) -> int:
        return self._tg_object.from_user.id
