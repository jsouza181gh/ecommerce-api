from fastapi import APIRouter, Response, status
from uuid import UUID

from ..schemas import UserSchema, SaveUserSchema, AuthTokensName
from .dependencies import CurrentUser, UserDependencies

router = APIRouter(prefix='/users', tags=['Users'])

@router.get(
    '/{user_id}',
    response_model=UserSchema,
    status_code=status.HTTP_200_OK
)
async def get_user(
    user_id: UUID,
    current_user: CurrentUser,
    user_service: UserDependencies
):
    user = await user_service.find_by_id(user_id, current_user)

    return user


@router.get(
    '/',
    response_model=list[UserSchema],
    status_code=status.HTTP_200_OK
)
async def list_users(
    current_user: CurrentUser,
    user_service: UserDependencies
):
    users = await user_service.find_all(current_user)

    return users


@router.put(
    '/{user_id}',
    response_model=UserSchema
)
async def update_user(
    user_id: UUID,
    payload: SaveUserSchema,
    current_user: CurrentUser,
    user_service: UserDependencies
):
    new_user = await user_service.update(user_id, payload, current_user)

    return new_user


@router.put(
    '/activate/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def activate_user(
    user_id: UUID,
    current_user: CurrentUser,
    user_service: UserDependencies
):
    await user_service.activate(user_id, current_user)


@router.delete(
    '/deactivate/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def deactivate_user(
    user_id: UUID,
    current_user: CurrentUser,
    user_service: UserDependencies,
    response: Response
):
    await user_service.deactivate(user_id, current_user)

    response.delete_cookie(key=AuthTokensName.ACCESS_TOKEN)
    response.delete_cookie(key=AuthTokensName.REFRESH_TOKEN)



@router.delete(
    '/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
    user_id: UUID,
    current_user: CurrentUser,
    user_service: UserDependencies
):
    await user_service.delete(user_id, current_user)