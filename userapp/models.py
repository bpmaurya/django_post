from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email,first_name,last_name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, first_name,last_name, email, password):
        """
       Creates and saves a staff user with the given email and password.
       """
        user = self.create_user(
            email,
            first_name, 
            last_name,
            password=password,
        )
        user.first_name = first_name
        user.last_name = last_name
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email,first_name,last_name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
        )
        user.first_name = first_name
        user.last_name = last_name
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    objects = UserManager()
    first_name = models.CharField(max_length=12)
    last_name = models.CharField(max_length=23)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
        )
    username = None
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_first_name(self):
        # The user is identified by their email address
        return self.first_name

    def get_last_name(self):
        # The user is identified by their email address
        return self.last_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin     
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=233)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} {self.text}'
