from bson.objectid import ObjectId

from starlette.responses import JSONResponse
from starlette.endpoints import HTTPEndpoint
from starlette.authentication import requires

from src.models.Permissions import AuthenticationScopes
from src.ErrorHandler import Error, ErrorType
from src.database.db_mongo import users_collection
from src import strings

from src.models.User import User


class UsersController(HTTPEndpoint):
    @requires(AuthenticationScopes.authenticated)
    async def get(self, request):
        users = await get_users()
        return JSONResponse([u.serialized for u in users])

class UserController(HTTPEndpoint):
    @requires(AuthenticationScopes.authenticated)
    async def get(self, request):
        id = request.path_params['user_id']
        user = await get_user(id)

        if user:
            return JSONResponse(user.serialized)
        else:
            raise Error(ErrorType.not_found, strings.USER_NOT_FOUND)

    @requires(AuthenticationScopes.authenticated)
    async def put(self, request):
        id = request.path_params['user_id']
        json = await request.json()
        user = await get_user(id)

        if user:
            user.update(json)
            return JSONResponse(user)
        else:
            raise Error(ErrorType.generic, 'Error updating user')


async def get_user(id) -> User:
    user = users_collection.find_one({'_id': ObjectId(id)})
    return User(**user) if user else None


async def get_users(filter: dict = {}):
    return [User(**x) for x in users_collection.find(filter)]
