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
    """A simple article model"""

    STYLE_CHOICES = [
        ('v-strap', 'V-STRAP'),
        ('sandal', 'SANDAL'),
        ('t-strap', 'T-STRAP'),
        ('covering', 'COVERING'),
        ('shoes', 'SHOES'),
        ('', 'None'),
    ]
    BRAND_CHOICES = [
        ('pride', 'Pride'),
        ('debongo', 'Debongo'),
        ('smartak', 'Smartak'),
        ('stile', 'Stile'),
        ('lpride', 'L. Pride'),
        ('disney', 'Disney'),
        ('batman', 'Batman'),
        ('kapers', 'Kapers'),
        ('', 'None'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
    )
    artno = models.CharField(max_length=6, unique=True)
    brand = models.CharField(max_length=25, choices=BRAND_CHOICES, blank=True)
    style = models.CharField(max_length=25, choices=STYLE_CHOICES, blank=True)

    def __str__(self):
        return self.artno


class ArticleDetail(models.Model):
    """
    More detailed model of article. color, category wise informations.
    """

    CATEGORY_CHOICES = [
        ('gents', 'Gents'),
        ('ladies', 'Ladies'),
        ('boys', 'Boys'),
        ('kids', 'Kids'),
        ('children', 'Children'),
        ('giants', 'Giants'),
        ('infant', 'Infant')
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
    )
    article = models.ForeignKey(
        Article,
        related_name='details',
        on_delete=models.CASCADE
    )
    color = models.ForeignKey(Color, on_delete=models.CASCADE)

    category = models.CharField(max_length=10)
    artid = models.CharField(max_length=12, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    basic = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)
    export = models.BooleanField(default=False)

    def __str__(self):
        return self.artid
