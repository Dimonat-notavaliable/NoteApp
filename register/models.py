from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.CharField(
        _("email"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer."
        ),
        validators=[validate_email],
        error_messages={
            "unique": _("Пользователь с такой почтой уже существует."),
        })
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
