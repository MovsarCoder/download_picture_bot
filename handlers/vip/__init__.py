from aiogram import Router
router = Router()


from .handlers.vip_panel_handler import router as main_vip_router
from .handlers.vip_panel_super_cashback_handler import router as super_cashback_router
from .handlers.vip_panel_ordinary_cashback_handler import router as ordinary_cashback_router
from .handlers.vip_panel_pars_all_product_handler import router as pars_all_router
from .handlers.buy_vip_panel import router as buy_vip_router
from .handlers.info_vip_panel_handler import router as vip_panel_info_router

router.include_router(main_vip_router)
router.include_router(super_cashback_router)
router.include_router(ordinary_cashback_router)
router.include_router(pars_all_router)
router.include_router(buy_vip_router)
router.include_router(vip_panel_info_router)
