
from django.db import models
from django.core import signing


class PasswordMixin(object):
    password_encrypted = models.CharField(max_length=128, null=False, blank=False)

    @property
    def password(self):
        return signing.loads(self.password_encrypted)

    @password.setter
    def password(self, value):
        self.password_encrypted = signing.dumps(value)
