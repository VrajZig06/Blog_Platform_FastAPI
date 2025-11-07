from fastapi import APIRouter

auth_router = APIRouter(
    prefix="/auth"
)

@auth_router.post("/login")
def login_user():
    pass