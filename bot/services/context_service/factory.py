from aiogram.dispatcher.fsm.context import FSMContext

from bot.services.context_service.context_service import ContextService


def create_context_service(state: FSMContext) -> ContextService:
    return ContextService(state)
