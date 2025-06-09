from aiogram import Router
router = Router()


from .video.download_video_handler import router as download_video_router
from .picture.download_picture_handler import router as download_picture_router

router.include_router(download_video_router)
router.include_router(download_picture_router)

