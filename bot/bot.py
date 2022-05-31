from typing import Optional, Union
from aiogram import Bot
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

class TGBot(Bot):
    async def send(self,
                   chat_id: int,
                   text: str,
                   reply_markup: Optional[
                                    Union[
                                        ReplyKeyboardMarkup,
                                        ReplyKeyboardRemove,
                                    ]
                                 ] = None,):
        return await self.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup
        )
