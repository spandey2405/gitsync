import hashlib
from django.core import exceptions as django_exc
from rest_framework.status import HTTP_400_BAD_REQUEST
from src.common.libraries.constants import *
from src.common.models import User , Token

class UserLib():
    def password_hashing(self, password_hash, salt=None):
        if not salt:
            salt = User.objects.generate_salt()
        salted_client_hash = str(password_hash + salt)
        hash_library = hashlib.new(HASH_METHOD_USER_ADD)
        hash_library.update(salted_client_hash)
        server_hash = hash_library.hexdigest()
        return (server_hash, salt)


    def is_unique_email(self, email):
        if not User.objects.filter(email=email).exists():
           return True
        raise django_exc.ValidationError('email address already exists', code=HTTP_400_BAD_REQUEST)

    def add_user(self, user_details):
        response = dict()
        if self.is_unique_email(user_details[KEY_EMAIL_ID]):
            try:
                server_hash, salt = self.password_hashing(user_details[KEY_PASSWORD_HASH])
                user_details[KEY_PASSWORD_HASH] = server_hash
                AddRequest =  User.objects.create(**user_details)
                return "User Added"
            except Exception as e:
                print e


    def login(self, signin_details):
        email = signin_details[KEY_EMAIL_ID]
        password_hash = signin_details[KEY_PASSWORD_HASH]

        try:
            user = User.objects.get(email=email)
        except Exception as e:
            raise django_exc.ValidationError('Invalid Email Address', code=HTTP_400_BAD_REQUEST)

        hashed_salted_client_hash, salt = self.password_hashing(password_hash=password_hash, salt=user.salt)
        hash_stored_in_db = user.password_hash

        print hash_stored_in_db
        print hashed_salted_client_hash
        print password_hash
        print user.salt

        if hash_stored_in_db == hashed_salted_client_hash:
            token, created = Token.objects.get_or_create(user=user)
            return (token. access_token, created)

        raise django_exc.ValidationError('Invalid Password', code=HTTP_400_BAD_REQUEST)