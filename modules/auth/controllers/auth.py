from fastapi import APIRouter, status, Response

from ..schemas import AuthTokenSchema, SaveUserSchema, LoginSchema, AuthTokensName
from .dependencies import AuthDependences, AccessToken, RefreshToken, CurrentUser

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post(
    '/signup',
    status_code=status.HTTP_201_CREATED
)
async def signup(
    payload: SaveUserSchema,
    auth_service: AuthDependences,
    response: Response
):
    auth_tokens = await auth_service.signup(payload)

    response.set_cookie(
        key=AuthTokensName.ACCESS_TOKEN, 
        value=auth_tokens.access_token,
        httponly=True,
        samesite="lax"
    )

    response.set_cookie(
        key=AuthTokensName.REFRESH_TOKEN,
        value=auth_tokens.refresh_token,
        httponly=True,
        samesite="lax"
    )


@router.post(
    '/signin',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def signin(
    payload: LoginSchema,
    auth_service: AuthDependences,
    response: Response
):
    auth_tokens = await auth_service.signin(payload)

    response.set_cookie(
        key=AuthTokensName.ACCESS_TOKEN, 
        value=auth_tokens.access_token,
        httponly=True,
        samesite="lax"
    )

    response.set_cookie(
        key=AuthTokensName.REFRESH_TOKEN,
        value=auth_tokens.refresh_token,
        httponly=True,
        samesite="lax"
    )


@router.post(
    '/signout',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[CurrentUser]
)
async def signout(
    access_token: AccessToken,
    refresh_token: RefreshToken,
    auth_service: AuthDependences,
    response: Response
):
    auth_tokens = AuthTokenSchema(
        access_token=access_token,
        refresh_token=refresh_token
    )

    await auth_service.signout(auth_tokens)

    response.delete_cookie(key=AuthTokensName.ACCESS_TOKEN)
    response.delete_cookie(key=AuthTokensName.REFRESH_TOKEN)


@router.post(
    '/refresh',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def refresh(
    access_token: AccessToken,
    refresh_token: RefreshToken,
    auth_service: AuthDependences,
    response: Response
):
    auth_tokens = AuthTokenSchema(
        access_token=access_token,
        refresh_token=refresh_token
    )

    refreshed_tokens = await auth_service.refresh(auth_tokens)

    response.set_cookie(
        key=AuthTokensName.ACCESS_TOKEN,
        value=refreshed_tokens.access_token,
        httponly=True,
        samesite="lax"
    )

    response.set_cookie(
        key=AuthTokensName.REFRESH_TOKEN,
        value=refreshed_tokens.refresh_token,
        httponly=True,
        samesite="lax"
    )