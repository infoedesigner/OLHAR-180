from django.urls import reverse
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView

from nxt.security.models import User
from nxt.security.mixins import AdminRequiredMixin, ClientViewMixin, IsStaffRequiredMixin
from nxt.security.forms import ClientUserForm, SearchUserForm, UserForm, UserCompanyForm

class UserListView(AdminRequiredMixin, generic.ListView):

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['form'] = SearchUserForm(data=self.request.GET or None)
        return context

    def get_queryset(self):
        form = SearchUserForm(data=self.request.GET or None)
        return form.search(User.
            objects.filter(company=self.request.user.company, profile='funcionario')
        )

    def post(self, request):
        user_id = request.POST.get('id')
        action = request.POST.get('action')
        if action in ['deactive', 'active'] and user_id:
            user = get_object_or_404(self.get_queryset(), pk=user_id)
            user.is_active = action == 'active'
            user.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
        return redirect('security:user_list')

class UserCreateView(AdminRequiredMixin, generic.CreateView):

    form_class = UserForm
    template_name = 'security/user_form.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.created_by = self.request.user
        user.company = self.request.user.company
        user.profile = 'funcionario'
        user.is_active = True
        user.save()
        form.save_m2m()
        messages.success(self.request, 'Usuário adicionado com sucesso!')
        return redirect('security:user_list')


class UserUpdateView(AdminRequiredMixin, generic.UpdateView):

    form_class = UserForm

    def get_queryset(self):
        return User.objects.filter(company=self.request.user.company)

    def get_success_url(self):
        messages.success(self.request, 'Usuário atualizado com sucesso!')
        return reverse('security:user_list')


class ClientUserListView(AdminRequiredMixin, ClientViewMixin, generic.ListView):

    paginate_by = 10
    template_name = 'security/client_user_list.html'

    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['form'] = SearchUserForm(data=self.request.GET or None)
        return context

    def get_queryset(self):
        form = SearchUserForm(data=self.request.GET or None)
        return form.search(
            User.objects.filter(client=self.client, profile='cliente')
        )


class ClientUserCreateView(AdminRequiredMixin, ClientViewMixin, generic.CreateView):

    form_class = ClientUserForm
    template_name = 'security/client_user_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['client'] = self.client
        return kwargs

    def form_valid(self, form):
        user = form.save(commit=False)
        user.created_by = self.request.user
        user.client = self.client
        user.company = self.client.company
        user.profile = 'cliente'
        user.is_active = True
        user.save()
        messages.success(self.request, 'Usuário adicionado com sucesso!')
        return redirect('security:client_user_list', pk=self.client.pk)


class ClientUserUpdateView(AdminRequiredMixin, ClientViewMixin, generic.UpdateView):

    form_class = ClientUserForm
    template_name = 'security/client_user_form.html'
    pk_url_kwarg = 'client'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['client'] = self.client
        return kwargs

    def get_queryset(self):
        return User.objects.filter(client=self.client)

    def get_success_url(self):
        messages.success(self.request, 'Usuário atualizado com sucesso!')
        return redirect('security:client_user_list', pk=self.client.pk)


class PasswordChangeView(AdminRequiredMixin, generic.FormView):

    form_class = PasswordChangeForm
    template_name = 'security/password_change.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, 'Senha alterada com sucesso!')
        return redirect('core:index')


class UpdateMeView(AdminRequiredMixin, generic.UpdateView):

    form_class = UserForm
    template_name = 'security/user_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        del form.fields['nxt_permissions']
        return form

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, 'Seus dados foram atualizados com sucesso!')
        return reverse('core:index')


class UserCompanyUpdateView(IsStaffRequiredMixin, generic.View):

    def post(self, request):
        form = UserCompanyForm(instance=request.user, data=request.POST)
        if form.is_valid():
            messages.success(self.request, 'Empresa atualizada com sucesso!')
            form.save()
        return redirect('core:index')


class ClientLoginView(LoginView):
    template_name = 'security/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        print(self.request.user.profile)
        if self.request.user.profile == 'cliente':
            client = self.request.user.client
            return redirect(reverse('clients:clipping_list', kwargs={'slug': client.slug}))
        return response

user_list = UserListView.as_view()
user_create = UserCreateView.as_view()
user_update = UserUpdateView.as_view()
client_user_list = ClientUserListView.as_view()
client_user_create = ClientUserCreateView.as_view()
client_user_update = ClientUserUpdateView.as_view()
password_change = PasswordChangeView.as_view()
update_me = UpdateMeView.as_view()
user_company_update = UserCompanyUpdateView.as_view()
