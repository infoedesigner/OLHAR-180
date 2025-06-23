from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect

from nxt.security.mixins import AdminRequiredMixin

from nxt.notifications.models import NotificationModel
from nxt.notifications.forms import NotificationModelForm


class NotificationListView(AdminRequiredMixin, generic.ListView):

    template_name = 'notifications/notification_model_list.html'

    def get_queryset(self):
        return NotificationModel.objects.filter(company=self.request.user.company)


class NotificationCreateView(AdminRequiredMixin, generic.CreateView):

    template_name = 'notifications/notification_model_form.html'
    form_class = NotificationModelForm

    def form_valid(self, form):
        notification_model = form.save(commit=False)
        notification_model.company = self.request.user.company
        notification_model.save()
        messages.success(self.request, 'Modelo de notificação criado com sucesso!')
        return redirect('notifications:notification_model_list')


class NotificationUpdateView(AdminRequiredMixin, generic.UpdateView):

    template_name = 'notifications/notification_model_form.html'
    form_class = NotificationModelForm

    def get_queryset(self):
        return NotificationModel.objects.filter(company=self.request.user.company)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Modelo de notificação atualizado com sucesso!')
        return redirect('notifications:notification_model_list')


notification_model_list = NotificationListView.as_view()
notification_model_create = NotificationCreateView.as_view()
notification_model_update = NotificationUpdateView.as_view()
