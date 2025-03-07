from aiogram import Router
from handler.media.picture.download_picture_handler import router as picture_handler
from handler.media.video.download_video_handler import router as video_handler
from handler.commands.start_command import router as start_command
from handler.commands.help_command import router as help_command
from handler.commands.profile_command import router as profile_command
from handler.admin.handlers.admin_handler import router as admin_handler
from handler.vip.handlers.buy_vip_panel import router as buy_vip_panel
from handler.vip.handlers.vip_panel_handler import router as vip_panel_router
from handler.vip.handlers.vip_panel_ordinary_cashback_handler import router as ordinary_cashback_router
from handler.vip.handlers.vip_panel_super_cashback_handler import router as super_cashback_router
from handler.vip.handlers.vip_panel_pars_all_product_handler import router as pars_all_product_router

router = Router()



router.include_router(start_command)
router.include_router(help_command)
router.include_router(profile_command)


router.include_router(picture_handler)
router.include_router(video_handler)

router.include_router(admin_handler)


router.include_router(buy_vip_panel)
router.include_router(vip_panel_router)
router.include_router(ordinary_cashback_router)
router.include_router(super_cashback_router)
router.include_router(pars_all_product_router)
