# from aiogram import Router
# from handlers.media.picture.download_picture_handler import router as picture_handler
# from handlers.media.video.download_video_handler import router as video_handler
# from handlers.commands.start_command import router as start_command
# from handlers.commands.help_command import router as help_command
# from handlers.commands.profile_command import router as profile_command
# from handlers.admin.handlers.admin_handler import router as admin_handler
# from handlers.admin.handlers.newsletter_handler import router as newsletter_router
# from handlers.vip.handlers.buy_vip_panel import router as buy_vip_panel
# from handlers.vip.handlers.vip_panel_handler import router as vip_panel_router
# from handlers.vip.handlers.vip_panel_ordinary_cashback_handler import router as ordinary_cashback_router
# from handlers.vip.handlers.vip_panel_super_cashback_handler import router as super_cashback_router
# from handlers.vip.handlers.vip_panel_pars_all_product_handler import router as pars_all_product_router


# router = Router()
#
#
#
# router.include_router(start_command)
# router.include_router(help_command)
# router.include_router(profile_command)
#
#
# router.include_router(picture_handler)
# router.include_router(video_handler)
#
# # router.include_router(admin_handler)
# router.include_router(newsletter_router)
#
#
# router.include_router(buy_vip_panel)
# router.include_router(vip_panel_router)
# router.include_router(ordinary_cashback_router)
# router.include_router(super_cashback_router)
# router.include_router(pars_all_product_router)


from aiogram import Router
router = Router()


# Подключение всех Routers из админки
from handlers.admin import router as all_admin_routers
router.include_router(all_admin_routers)


# Подключение всех Routers из команд
from handlers.commands import router as all_commands_routers
router.include_router(all_commands_routers)


# Подключение всех Routers из media (Скачивание фоток и видео)
from handlers.media import router as all_media_routers
router.include_router(all_media_routers)


# Подключение всех Routers из Vip
from handlers.vip import router as all_vip_routers
router.include_router(all_vip_routers)
