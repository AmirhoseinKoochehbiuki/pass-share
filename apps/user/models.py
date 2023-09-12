from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from user.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()
    username = models.CharField(max_length=100)
    email = models.EmailField(blank=True, unique=True)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self) -> str:
        return self.first_name + self.last_name
