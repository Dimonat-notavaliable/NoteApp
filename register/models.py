from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _


class Color(models.Model):
    COLOR_PALETTE = [
        ("#FFFF0090", "yellow",),
        ("#FF000090", "red",),
        ("#00FF0090", "green",),
        ("#0000FF90", "blue",),
        ("#FF00FF90", "magenta",),
        ("#00FFFF90", "cyan",),
    ]
    hex = models.CharField('HEX', max_length=10, choices=COLOR_PALETTE)
    name = models.CharField(max_length=40, default=None, null=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_absolute_url():
        return '/'

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'


class ColorPreference(models.Model):
    high_importance = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='high')
    medium_importance = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='medium')
    low_importance = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='low')
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        slug = self.high_importance.name + self.medium_importance.name + self.low_importance.name
        if ColorPreference.objects.filter(slug=slug).exists():
            self.pk = ColorPreference.objects.get(slug=slug).id
        self.slug = slug
        super(ColorPreference, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Цветовая схема'
        verbose_name_plural = 'Цветовые схемы'


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
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    preference = models.ForeignKey(ColorPreference, on_delete=models.SET_NULL, related_name='user',
                                   blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.preference is not None:
            self.preference.save()
        super(User, self).save(*args, **kwargs)
