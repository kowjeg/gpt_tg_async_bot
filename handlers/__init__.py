from aiogram import Router

from .commands_handler import router as commands_router
from .callbacks_handler import router as callbacks_router
from .random_fact import router as rand_router
from .gpt_chat import router as gpt_router
from .talk import router as talk_router
from .quiz import router as quiz_router


router = Router()
router.include_routers(commands_router, callbacks_router, rand_router, gpt_router, talk_router, quiz_router)