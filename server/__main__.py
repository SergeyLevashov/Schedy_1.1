from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from handlers import setup_routers
from api import common

from config_reader import config, dp, app

dp.include_router(setup_routers())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(common.router)

if __name__ == "__main__":
    uvicorn.run(app, host=config.APP_HOST, port=config.APP_PORT)