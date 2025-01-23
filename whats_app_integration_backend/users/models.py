import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid

class Roles(models.TextChoices):
    SUPER_ADMIN = 'SUPER_ADMIN', _('Super Admin')
    ADMIN = 'ADMIN', _('Admin')
    READ_ONLY_USER = 'READ_ONLY_USER', _('Read Only User')

def generate_random_phone_number():
    """Generates a random phone number in the format +XXXXXXXXXXXX."""
    country_code = "+" + "".join(random.choices(string.digits, k=random.randint(1, 3)))  # Country code (1-3 digits)
    number = "".join(random.choices(string.digits, k=9))  # 9-digit number
    return country_code + number

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.READ_ONLY_USER
    )
    created_date = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True) # Add phone number field

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    groups = None
    user_permissions = None

    def save(self, *args, **kwargs):
        if not self.phone_number:  # Only generate if phone number is not set
            while True:
                potential_phone_number = generate_random_phone_number()
                if not User.objects.filter(phone_number=potential_phone_number).exists():
                    self.phone_number = potential_phone_number
                    break
        super().save(*args, **kwargs)

    def is_super_admin(self):
        return self.role == Roles.SUPER_ADMIN or self.is_superuser

    def is_admin_user(self):
        return self.role in [Roles.ADMIN, Roles.SUPER_ADMIN]

    def is_read_only_user(self):
        return self.role == Roles.READ_ONLY_USER

    def __str__(self):
        return self.username