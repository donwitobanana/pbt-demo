from fastapi import FastAPI

from pbt_demo.items import router

app = FastAPI()
app.include_router(router)
