from fastapi import APIRouter

router = APIRouter()

@router.get("/users/", tags=["users"])
def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]