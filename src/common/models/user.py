from django.db import models
from src.common.libraries.constants import *
import binascii, os, uuid


class UserManager(models.Manager):
    def generate_userid(self):
        return str(uuid.uuid4())

    def generate_salt(self):
        return binascii.hexlify(os.urandom(SALT_LENGTH/2)).decode()

class User(models.Model):
    email = models.EmailField(max_length=MAX_EMAIL_LENGTH, unique=True)
    password_hash = models.CharField(max_length=MAX_PASSWORD_LENGTH)
    user_id = models.CharField(max_length=UID_LENGTH, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    salt = models.CharField(max_length=SALT_LENGTH)
    objects = UserManager()

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = User.objects.generate_userid()
        if not self.salt:
            self.salt = User.objects.generate_salt()
        return super(User, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user_id

    class Meta:
        db_table = 'user'
        app_label = 'common'