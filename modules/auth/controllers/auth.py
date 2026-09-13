from fastapi import APIRouter, status

from ..schemas import AuthTokenSchema, SaveUserSchema, LoginSchema
from .dependencies import AuthDependences, Authenticated

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post(
    '/signup',
    response_model=AuthTokenSchema,
    status_code=status.HTTP_201_CREATED
)
async def signup(
    payload: SaveUserSchema,
    auth_service: AuthDependences
):
    auth_tokens = await auth_service.signup(payload)

    return auth_tokens


@router.post(
    '/signin',
    response_model=AuthTokenSchema,
    status_code=status.HTTP_200_OK
)
async def signin(
    payload: LoginSchema,
    auth_service: AuthDependences
):
    auth_tokens = await auth_service.signin(payload)

    return auth_tokens


@router.post(
    '/signout',
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Authenticated]
)
async def signout(
    payload: AuthTokenSchema,
    auth_service: AuthDependences
):
    await auth_service.signout(payload)


@router.post(
    '/refresh',
    response_model=AuthTokenSchema,
    status_code=status.HTTP_200_OK
)
async def refresh(
    payload: AuthTokenSchema,
    auth_service: AuthDependences
):
    auth_tokens = await auth_service.refresh(payload)

    return auth_tokens