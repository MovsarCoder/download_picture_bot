from aiogram import Router

router = Router()

from .handlers.admin_handler import router as admin_handler
from .handlers.newsletter_handler import router as newsletter_handler
from .handlers.add_admin_handler import router as add_admin_handler
from .handlers.remove_admin_handlers import router as remove_admin_handler
from .handlers.add_new_group_handler import router as add_new_group_handler
from .handlers.delete_group_handler import router as remove_group_handler
from .handlers.list_group_handler import router as list_group_handler
from .handlers.add_new_user_vip_handler import router as add_new_vip_user_handler


router.include_router(admin_handler)
router.include_router(newsletter_handler)
router.include_router(add_admin_handler)
router.include_router(remove_admin_handler)
router.include_router(add_new_group_handler)
router.include_router(remove_group_handler)
router.include_router(list_group_handler)
router.include_router(add_new_vip_user_handler)




