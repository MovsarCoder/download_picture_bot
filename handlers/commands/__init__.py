from aiogram import Router

router = Router()

from .handlers.help_command import router as help_command_router
from .handlers.profile_command import router as profile_command_router
from .handlers.start_command import router as start_command_router

router.include_router(help_command_router)
router.include_router(profile_command_router)
router.include_router(start_command_router)
