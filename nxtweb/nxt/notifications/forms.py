from django import forms

from nxt.notifications.models import NotificationModel


class NotificationModelForm(forms.ModelForm):

    class Meta:
        model = NotificationModel
        fields = [
            'title',
            'notification_type',
            'content',
        ]
