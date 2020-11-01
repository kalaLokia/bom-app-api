"""
Core models for the api
"""
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, \
                                        PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):
    """User manager for creating basic, super user"""
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


class Category(models.TextChoices):
    """
    Category choices, enum model. Human-readable name is default,
    (capitalized variable name)
    """
    GENTS = 'g'
    LADIES = 'l'
    GIANTS = 'x'
    KIDS = 'k'
    BOYS = 'b'
    GIRLS = 'r'
    CHILDREN = 'c'


def categorize(value):
    """ Main categories from category"""
    categories = {
        'g': 'gents',
        'l': 'ladies',
        'x': 'giants',
        'c': 'kids',
        'b': 'kids',
        'r': 'kids',
        'k': 'kids'
    }
    return categories.get(value, 'unknown')


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
        ('shoes', 'SHOES')
    ]
    BRAND_CHOICES = [
        ('pride', 'Pride'),
        ('debongo', 'Debongo'),
        ('smartak', 'Smartak'),
        ('stile', 'Stile'),
        ('lpride', 'L. Pride'),
        ('disney', 'Disney'),
        ('batman', 'Batman'),
        ('kapers', 'Kapers')
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


class ArticleInfo(models.Model):
    """
    More detailed model of article. color, category wise informations.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
    )
    article = models.ForeignKey(
        Article,
        related_name='items',
        on_delete=models.CASCADE
    )
    # TODO: articleid : full details of artid for filtering, search
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    category = models.CharField(max_length=1, choices=Category.choices)
    mcategory = models.CharField(max_length=10, default="unknown")
    artid = models.CharField(max_length=12, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    basic = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)
    export = models.BooleanField(default=False)

    def __str__(self):
        return self.artid


class Uom(models.TextChoices):
    """
    All Available Unit of Measurments
    """
    PAIR = 'pairs'
    KILOGRAM = 'kilogram'
    METER = 'meter'
    CONE = 'cone'
    ROLL = 'roll'
    NOS = 'nos'
    GRAM = 'gram'


class Material(models.Model):
    """
    Materials model
    """

    CATEGORY_CHOICES = [
        ('rexin', 'Rexin'),
        ('component', 'Component'),
        ('chemical', 'Chemical'),
        ('packing', 'Packing')
    ]

    code = models.CharField(max_length=18, unique=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=25, choices=CATEGORY_CHOICES,
                                blank=True)
    subcategory = models.CharField(max_length=25, blank=True)
    uom = models.CharField(max_length=15, choices=Uom.choices, blank=True)
    purchaseuom = models.CharField(max_length=15, choices=Uom.choices,
                                   blank=True)
    # cf - Conversion Factor
    cf = models.DecimalField(max_digits=12, decimal_places=4, default=1)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
