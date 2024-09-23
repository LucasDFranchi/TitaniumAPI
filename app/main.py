from fastapi import FastAPI


from routers import item_router, config_router

app = FastAPI()

app.include_router(item_router.router)
# app.include_router(config_router.router)
