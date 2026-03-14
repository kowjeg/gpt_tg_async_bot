from aiogram import Router

from .commands_handler import router as commands_router


router = Router()
router.include_routers(commands_router)