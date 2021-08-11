from datetime import datetime, timedelta
from django.conf import settings 
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth import password_validation
from django.utils import timezone
import jwt
        
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, is_active=True):
        """
        Creates and saves a User.
        """
        user = self.model(username=username, is_active=is_active)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, is_active=True, password=None):
        """
        Creates and saves a superuser.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(username=username, password=password, is_active=is_active)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # unique username.
    username = models.EmailField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    # instead of deleting an account.
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(default=timezone.now)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()
    # USERNAME_FIELD sets username used to log in.
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [is_active] # Password is required by default.

    def __str__(self):
        """ string in terminal """
        return self.username

    def get_full_name(self):
        # The user identified 
        return f"{self.firstname} {self.lastname}"

    def get_short_name(self):
        # The user identified 
        return self.username

    @property
    def token(self):
        """ Get token via user.token instead of user._generate_jwt_token(). """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """ Generates JSON web token identifiying the user and valid 1 day """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class Profile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,default=1,related_name='profile')

    class Meta:
        db_table='Profile'