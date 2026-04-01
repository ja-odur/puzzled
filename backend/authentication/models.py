from django.db import models, transaction
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core import signing
from django.utils.translation import ugettext_lazy as _
import pytz
from . import constants
from backend.email.factories.email_builder import EmailSender
from backend.lib.exceptions import FieldValidationError
from backend.lib.validators import validate_email, url_validator
from backend.lib.urltools import reverse_absolute


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.

        """
        picture_url = extra_fields.pop('picture_url', '').strip()

        if not email:
            raise ValueError('The given email must be set')
        if not validate_email(email):
            raise FieldValidationError('Not a valid email address', 'email', email)
        email = self.normalize_email(email)

        if picture_url:
            try:
                url_validator(picture_url)
            except Exception:
                raise FieldValidationError('Not a valid url', 'picture_url', picture_url)

        with transaction.atomic(using=self._db):
            user = self.model(email=email, **extra_fields)
            if password is not None:
                user.set_password(password)
            else:
                user.set_unusable_password()
            user.save(using=self._db)

        context_data = {
            'name': user.name,
            'verification_url': user.generate_email_confirmation_url(user.email),
        }
        user.send_email('Email Verification', 'verify_email', context_data)

        return user

    def create_user(self, email, password=None, **extra_fields):

        first_name = extra_fields.pop('first_name', '').strip().capitalize()
        last_name = extra_fields.pop('last_name', '').strip().capitalize()
        name = u'{} {}'.format(first_name, last_name).strip()

        extra_fields.setdefault('name', name)
        extra_fields.setdefault('preferred_name', first_name)

        timezone = extra_fields.pop('timezone', 'Africa/Kampala').strip()
        try:
            timezone = pytz.timezone(timezone)
        except pytz.exceptions.UnknownTimeZoneError:
            timezone = pytz.timezone('Africa/Kampala')

        extra_fields.setdefault('timezone', timezone.zone)

        user = self._create_user(email, password=password, **extra_fields)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    name = models.TextField()
    preferred_name = models.TextField(default='')
    email = models.TextField(_('email address'), unique=True)
    email_verified = models.BooleanField(default=False)
    telephone = models.TextField(blank=True, null=True)
    picture_url = models.TextField(blank=True, null=True)

    timezone = models.TextField(
        _('Timezone'), choices=zip(pytz.all_timezones, pytz.all_timezones), default='Africa/Kampala'
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    NAME_FIELD = 'name'

    def generate_email_confirmation_url(self, new_email):
        data = {
            'id': self.id,
            'new_email': new_email,
        }

        signed_data = signing.dumps(data)

        return reverse_absolute('authentication:verify_email', args=(signed_data,))

    def send_email(self, subject, template, context):
        EmailSender.DJANGO_MAIL.send_template_mail([self.email], subject, template, context)

    def confirm_email(self, signed_data, max_age=settings.VERIFY_EMAIL_LINK_AGE):
        error, message = True, None

        try:
            data = signing.loads(signed_data, max_age=max_age)
        except signing.SignatureExpired:
            message = constants.EXPIRED_LINK_MSG
            return error, message

        except signing.BadSignature:
            message = constants.INVALID_LINK_MSG
            return error, message

        if self.id != data['id']:
            message = constants.DIFFERENT_ACCOUNT_MSG
            return error, message

        if self.email != data['new_email']:
            message = constants.EMAIL_CHANGED_MSG
            return error, message

        self.email_verified = True
        self.save(update_fields=['email_verified'])
        error = False

        return error, message

    def __str__(self):
        short = self.name.strip()
        if short:
            return short
        else:
            return self.email

    def __repr__(self):
        return '<User email={!r}>'.format(self.email)
