from aiogram import Router

router = Router()


from handlers.commands.start_command import router as start_handler
router.include_router(start_handler)


from handlers.download_puctire_and_video.picture.download_picture_handler import router as picture_handler
from handlers.download_puctire_and_video.video.download_video_handler import router as video_handler
router.include_router(picture_handler)
router.include_router(video_handler)


from handlers.admin_panel.admin_handler import router as admin_handler
router.include_router(admin_handler)


from handlers.vip_panel.handlers.vip_panel_handler import router as vip_panel_router
from handlers.vip_panel.handlers.vip_panel_info_handler import router as vip_info_router
from handlers.vip_panel.handlers.vip_panel_ordinary_cashback_handler import router as ordinary_cashback_router
from handlers.vip_panel.handlers.vip_panel_super_cashback_handler import router as super_cashback_router
from handlers.vip_panel.handlers.vip_panel_pars_all_product_handler import router as pars_all_product_router
router.include_router(vip_panel_router)
router.include_router(vip_info_router)
router.include_router(ordinary_cashback_router)
router.include_router(super_cashback_router)
router.include_router(pars_all_product_router)
