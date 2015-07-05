from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class AccountManager(BaseUserManager):
    def create_user(self, username, email, password, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        if not username:
            raise ValueError('Users must have a username.')

        account = self.model(
            email=self.normalize_email(email),
            username=username
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, username, email, password, **kwargs):
        account = self.create_user(username, email, password, **kwargs)

        account.is_admin = True
        account.save()

        return account


class Account(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    avatar = ProcessedImageField(upload_to='avatars', format='JPEG', options={'quality': 80})

    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __unicode__(self):
        return self.email

    @property
    def date_joined(self):
        return self.created_at

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    def get_identification(self):
        return self.get_full_name() if self.first_name else self.username

    @models.permalink
    def get_edit_url(self):
        return ('edit-profile', (), {})

    @models.permalink
    def get_absolute_url(self):
        """Return absolute link"""
        return ('view-profile', (), {'username':  self.username})
