from rest_framework import generics
from rest_framework  import mixins
from rest_framework.status import HTTP_201_CREATED
from src.api.v1.libraries.customresponse import CustomResponse
from src.api.v1.libraries.loggingmixin import LoggingMixin
from src.api.v1.serializers.usersserializer import UsersSerializer
from src.common.libraries.pull.pullrequests import PullRequest
from src.api.v1.libraries.permissions import IsAuthenticatedOrCreate
from src.common.models.user import User
from src.common.libraries.constants import *
api_lib = PullRequest()
from django_mysqlpool import auto_close_db

'''
{
    "email": "saurabh.pandey@roder.in",
    "pass
}
'''

class PullRequestsView( LoggingMixin, generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin):
    model = User
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticatedOrCreate,)

    @auto_close_db
    def get(self, request):
        payload = api_lib.execute(request.GET.copy())
        return CustomResponse(message='User added', payload=payload, code=HTTP_201_CREATED)


