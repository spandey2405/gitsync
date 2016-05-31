from rest_framework import generics
from rest_framework  import mixins
from rest_framework.status import HTTP_201_CREATED
from src.api.v1.libraries.customresponse import CustomResponse
from src.api.v1.libraries.loggingmixin import LoggingMixin
from src.api.v1.serializers.usersserializer import UsersSerializer
from src.common.libraries.user.userlib import UserLib
from src.api.v1.libraries.permissions import IsAuthenticatedOrCreate
from src.common.models.user import User
from src.common.libraries.constants import *
user_lib = UserLib()
from django_mysqlpool import auto_close_db

'''
{
    "email": "saurabh.pandey@roder.in",
    "pass
}
'''

class UserView( LoggingMixin, generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin):
    model = User
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticatedOrCreate,)

    @auto_close_db
    def post(self, request):
        user_details = request.data.copy()
        payload = user_lib.add_user(user_details)
        return CustomResponse(message='User added', payload=payload, code=HTTP_201_CREATED)


