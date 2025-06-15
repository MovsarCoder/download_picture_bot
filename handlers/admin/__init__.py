from aiogram import Router

router = Router()

from .handlers.admin_handler import router as admin_handler
from .handlers.newsletter_handler import router as newsletter_handler
from .handlers.add_admin_handler import router as add_admin_handler

router.include_router(admin_handler)
router.include_router(newsletter_handler)
router.include_router(add_admin_handler)

