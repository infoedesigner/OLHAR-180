import datetime as dt

from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect


def last_access_middleware(get_response):
    def middleware(request):
        if request.user.is_authenticated:
            request.user.last_access = dt.datetime.now()
            request.user.save()
        response = get_response(request)
        return response
    return middleware


def expiration_access_middleware(get_response):
    def middleware(request):
        today = dt.date.today()
        if request.user.is_authenticated and request.user.expiration and today > request.user.expiration:
            logout(request)
            messages.error(request, 'Seu acesso está expirado!')
            return redirect('security:login')
        response = get_response(request)
        return response
    return middleware


class DisableCSRF(MiddlewareMixin):

    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
