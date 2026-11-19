from fastapi import FastAPI

from server.spp.routes.health import router as health_router
from server.spp.routes.pops import router as pops_router

app = FastAPI(
    title="POP Distribution System",
    description="Sistema centralizado de gerenciamento e distribuição de POPs",
    version="1.0.0"
)

app.include_router(health_router)
app.include_router(pops_router) 