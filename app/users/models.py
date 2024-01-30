from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    """
    Default custom user model for Makro Promo Bot.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class TelegramUser(models.Model):
    id = models.PositiveBigIntegerField(_("Телеграм ID"),
                                        db_index=True,
                                        primary_key=True,
                                        editable=False,
                                        auto_created=False
                                        )
    language = models.CharField(_("Язык пользователя"), max_length=2, blank=True, null=True)
    fullname = models.CharField(_("Имя пользователя"), max_length=100, blank=True, null=True)
    phone = models.CharField(_("Телефонный номер"), max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
