from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import signing
from django.shortcuts import redirect, render
from django.views.generic import View
from backend.lib.urltools import make_absolute
from backend.authentication import constants


class VerifyEmail(View):
    def get(self, request, signed_data, *args, **kwargs):
        try:
            signing.loads(signed_data, max_age=settings.VERIFY_EMAIL_LINK_AGE)
        except signing.SignatureExpired:
            message = constants.EXPIRED_LINK_MSG
            context = dict(message=message, redirect_url=make_absolute('/'))
            return render(self.request, 'notifications/error_notification.html', context=context)

        except signing.BadSignature:
            message = constants.INVALID_LINK_MSG
            context = dict(message=message, redirect_url=make_absolute('/'))
            return render(self.request, 'notifications/error_notification.html', context=context)

        if self.request.user.is_anonymous:
            self.request.session['verify_email_data'] = signed_data
            return redirect(settings.LOGIN_URL)

        user = get_user_model().objects.get(id=request.user.id)

        error, message = user.confirm_email(signed_data)

        if error:
            context = dict(message=message, redirect_url=make_absolute('/'))
            return render(self.request, 'notifications/error_notification.html', context=context)

        return redirect('/')
