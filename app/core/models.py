from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, \
                                        PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppport email instead username"""
    email = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Color(models.Model):
    """Colors to be used for article"""
    name = models.CharField(max_length=25, unique=True)
    # use validators for 2 char limit for code
    code = models.CharField(max_length=2, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return self.name


class Article(models.Model):
    """Article model"""

    STYLE_CHOICES = [
        ('v-strap', 'V-STRAP'),
        ('sandal', 'SANDAL'),
        ('t-strap', 'T-STRAP'),
        ('covering', 'COVERING'),
        ('shoes', 'SHOES'),
    ]
    CATEGORY_CHOICES = [
        ('g', 'Gents'),
        ('l', 'Ladies'),
        ('k', 'Kids'),
        ('c', 'Children'),
        ('b', 'Boys'),
        ('r', 'Girls'),
        ('x', 'Giants'),
        ('', 'None'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
    )
    artno = models.CharField(max_length=6, unique=True)
    # TODO make it choice field
    brand = models.CharField(max_length=25)
    style = models.CharField(max_length=25,
                             choices=STYLE_CHOICES)
    # TODO category to an array field
    category = models.CharField(max_length=10,
                                choices=CATEGORY_CHOICES, blank=True)
    colors = models.ManyToManyField('Color')
    # TODO article_detail => artno-color-category
    article_detail = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.artno
