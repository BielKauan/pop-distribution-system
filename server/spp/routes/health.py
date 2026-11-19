from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def home():
    return {
        "sistema": "POP Distribution System",
        "status": "online"
    }
