from django_mysqlpool import auto_close_db
from rest_framework import generics
from rest_framework import mixins
from rest_framework.status import HTTP_201_CREATED,HTTP_200_OK
from src.api.v1.libraries.customresponse import CustomResponse
from src.api.v1.libraries.loggingmixin import LoggingMixin
from src.api.v1.libraries.permissions import IsAuthenticatedOrCreate
from src.api.v1.serializers.usersserializer import UsersSerializer
from src.common.libraries.constants import *
from src.common.libraries.token.tokenlib import TokenLib
from src.common.libraries.user.userlib import UserLib
from src.common.models import User

user_lib = UserLib()
token_lib = TokenLib()

'''
{
    "email": "scoder91@gmail.com",
    "password_hash": "12345678"
}
'''

class TokenView(LoggingMixin, generics.GenericAPIView, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    model = User
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticatedOrCreate, )

    @auto_close_db
    def post(self, request):
        global user_lib, token_lib
        request = request.data.copy()
        try:
            access_token, created = user_lib.login(request=request)
            message='already logged in'
            if created:
                message = 'logged in'
        except Exception as e:
            print e
            message = "error"
            access_token = "NA"
        return CustomResponse(message=message, payload={'access_token':access_token}, code=HTTP_200_OK)

    @auto_close_db
    def delete(self, request):
        token_lib.delete_access_token(token=request.auth)
        return CustomResponse(message="logged out", code=HTTP_200_OK)