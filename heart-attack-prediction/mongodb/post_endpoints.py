from fastapi import APIRouter
from routes.heart_attack_tests import router as hat_router

router = APIRouter()

# Include POST-style routers (creates a grouping for POST operations)
router.include_router(hat_router)
