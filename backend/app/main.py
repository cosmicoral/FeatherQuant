from app.api.assets import router as assets_router

app.include_router(assets_router, prefix="/api")