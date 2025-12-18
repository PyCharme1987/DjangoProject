from enum import unique
from tokenize import blank_re

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import UserManager
from django.db import models
from random import randint

class Service:

    @staticmethod
    def generate_activation_code(size):
        list_ = [str(randint(0,9)) for i in range(size)]
        result = ''.join(list_)
        return result



class UserManager(BaseUserManager):
    def _create(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.update(
            {
                'is_staff': False,
                'is_active': False,
                'activation_code': Service.generate_activation_code(5)
            }
        )
        return self._create(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.update(
            {
                'is_staff': True,
                'is_active': True
            }
        )
        return self._create(email, password, **extra_fields)


class User(AbstractBaseUser):
    id = models.AutoField(unique=True, primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField()
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    nationality = models.CharField(blank=True, null=True)

    activation_code = models.CharField(blank=True, null=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def has_perm(self, obj):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    def get_info(self):
        return{
            'email': self.email,
            'username': self.username,
            'age': self.age,
            'nationality': self.nationality,
            'is_active': self.is_active,
            'is_staff': self.is_staff,
        }

    def send_activation_code(self):
        """
        theoretically here should be logic of sending email, but we are poor, thats why its very simple
        """
        print(
            f"""
            ==============================
            here is ur code, havara
            code - {self.activation_code}
            ==============================
            """
        )

    # def __str__(self):
    #     return f"{self.id}"
