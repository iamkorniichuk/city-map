from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **kwargs):
        user = self.model(phone_number=phone_number, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password=None, **kwargs):
        user = self.create_user(phone_number, password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(PermissionsMixin, AbstractBaseUser):
    phone_number = PhoneNumberField(
        unique=True,
        verbose_name=_("phone number"),
    )
    password = models.CharField(max_length=128, verbose_name=_("password"))

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return str(self.phone_number)
