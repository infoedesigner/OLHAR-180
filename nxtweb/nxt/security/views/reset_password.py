from django.views import generic
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import login
from django.contrib import messages

from nxt.security.models import User, ResetPassword
from nxt.security.forms import ResetPasswordForm, CheckResetPasswordForm


class ResetPasswordView(generic.FormView):

    form_class = ResetPasswordForm
    template_name = 'security/reset_password.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except:
            context = self.get_context_data(form=form)
            messages.error(self.request, 'Não foi encontrado nenhuma conta com o e-mail informado!')
        else:
            reset_password = form.save(user)
            return redirect('security:check_reset_password', pk=reset_password.pk)
        return self.render_to_response(context)


class CheckResetPasswordView(generic.FormView):

    form_class = CheckResetPasswordForm
    template_name = 'security/check_reset_password.html'

    @property
    def reset_password(self):
        _reset_password = getattr(self, '_reset_password', None)
        if _reset_password is None:
            self._reset_password = get_object_or_404(ResetPassword, pk=self.kwargs['pk'])
        return self._reset_password

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['reset_password'] = self.reset_password
        return kwargs

    def form_valid(self, form):
        return redirect('security:set_password', pk=self.reset_password.pk, code=form.cleaned_data['code'])


class SetPasswordView(generic.FormView):

    form_class = SetPasswordForm
    template_name = 'security/set_password.html'

    @property
    def reset_password(self):
        _reset_password = getattr(self, '_reset_password', None)
        if _reset_password is None:
            self._reset_password = get_object_or_404(
                ResetPassword, pk=self.kwargs['pk'], code=self.kwargs['code']
            )
        return self._reset_password

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.reset_password.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, 'django.contrib.auth.backends.ModelBackend')
        return redirect('core:index')


reset_password = ResetPasswordView.as_view()
check_reset_password = CheckResetPasswordView.as_view()
set_password = SetPasswordView.as_view()
