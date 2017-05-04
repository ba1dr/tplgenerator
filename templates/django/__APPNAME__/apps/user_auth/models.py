# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Account(AbstractUser):

    class Meta:
        ordering = ('id', )

    @property
    def is_admin(self):
        return self.is_superuser

    def get_identification(self):
        return self.get_full_name() if self.first_name else self.username
