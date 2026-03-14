from aiogram import Router

from .commands_handler import router as commands_router
from .callbacks_handler import router as callbacks_router

router = Router()
router.include_routers(commands_router, callbacks_router)