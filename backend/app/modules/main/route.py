from fastapi import APIRouter
from .controller import MainController

main_router = APIRouter(prefix="/api/v1/main", tags=["main"])
main_controller = MainController()


@main_router.get("/")
def index():
    return {"data": main_controller.index()}
      
