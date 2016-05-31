from src.api.v1.serializers.dynamicfieldmodelserializer import DynamicFieldsModelSerializer
from src.common.libraries.constants import *
from src.common.models.user import User
from rest_framework import serializers

class UsersSerializer(DynamicFieldsModelSerializer):
# class UsersSerializer(serializers.ModelSerializer):
    """
    Serializing all the Users
    """
    class Meta:
        model = User
        fields = (
            KEY_USER_ID,
            KEY_EMAIL_ID,
            KEY_USER_NAME,
        )

