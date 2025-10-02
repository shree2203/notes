import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, user_email, user_name, password=None, **extra_fields):
        if not user_email:
            raise ValueError("Email is required")
        user_email = self.normalize_email(user_email)
        user = self.model(user_email=user_email, user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_email, user_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(user_email, user_name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=100, unique=True)
    user_email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    last_update = models.DateTimeField(auto_now=True)
    create_on = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "user_email"
    REQUIRED_FIELDS = ["user_name"]

    objects = UserManager()

    def __str__(self):
        return self.user_email
