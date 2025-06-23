from http import client
from django import forms
from django.db.models import Q

from nxt.core.widgets import BooleanSelect

from .models import User, ResetPassword


class SearchUserForm(forms.Form):

    q = forms.CharField(label='Pesquisar', required=False)

    def search(self, queryset):
        if self.is_valid():
            q = self.cleaned_data.get('q')
            if q:
                queryset = queryset.filter(
                    Q(name__icontains=q) | Q(email__icontains=q)
                )
        return queryset

class UserAdminForm(forms.ModelForm):

    new_password = forms.CharField(
        label='Nova Senha', widget=forms.PasswordInput,
        required=False,
        help_text='Informe uma senha caso deseje alterar, caso contrário deixa esse campo em branco'
    )

    def save(self, commit=True):
        new_password = self.cleaned_data.get('new_password', '')
        if new_password:
            self.instance.set_password(new_password)
        return super().save(commit=commit)

    class Meta:
        model = User
        exclude = ['password']


class UserForm(forms.ModelForm):

    new_password = forms.CharField(
        label='Senha Inicial do usuário', widget=forms.PasswordInput,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            del self.fields['new_password']

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password', '')
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
            self.save_m2m()
        return user

    class Meta:
        model = User
        widgets = {
            'is_active': BooleanSelect,
        }
        fields = [
            'name',
            'is_active',
            'email',
            'phone',
            'nxt_permissions',
            'postal_code',
            'address',
            'number',
            'complement',
            'neighborhood',
            'city',
            'state',
            'bank',
            'bank_agency',
            'bank_number',
            'bank_operation',
            'bank_pix1',
            'bank_pix1_key_type',
            'bank_pix1_value',
            'bank_pix2',
            'bank_pix2_key_type',
            'bank_pix2_value',
            'birth_date',
            'mothers_name',
            'fathers_name',
            'naturalness',
            'naturalness_uf',
            'degree',
            'marital_status',
            'number_of_children',
            'childrens_names',
            'childrens_cpfs',
            'cpf',
            'rg',
            'rg_entity_uf',
            'rg_expedition',
            'work_card',
            'pis_pasep',
            'voter_registration',
            'driver_card',
            'driver_card_entity_uf',
            'driver_card_expedition',
            'home_phone',
            'whatsapp',
            'phone_message',
            'phone_contact',
            'photo',
            'internet_type',
            'internet_provider',
            'internet_contracted_speed',
            'internet_download_speed',
            'internet_upload_speed',
            'internet_others_providers',
            'internet_cost',
            'has_equipament',
            'equipament_type',
            'equipament_brand',
            'equipament_model',
            'equipament_processor',
            'equipament_memory',
            'equipament_hd',
            'equipament_brand',
            'equipament_hd_used',
            'equipament_has_dvr',
            'equipament_dvr_number',
            'equipament_dvr_description',
            'equipament_dvr_status',
            'equipament_dvr_local',
            'equipament_dvr_local_recorded',
            'equipament_dvr_total_channels',
        ]


class ClientUserForm(forms.ModelForm):

    new_password = forms.CharField(
        label='Senha Inicial do usuário', widget=forms.PasswordInput,
    )

    def __init__(self, client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = client
        if self.instance and self.instance.pk:
            del self.fields['new_password']

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password', '')
        user.profile = 'cliente'
        user.created_by = self.client.created_by
        user.client = self.client
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'phone',
            'expiration',
        ]

forms.ModelChoiceField

class UserCompanyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].queryset = self.instance.companies.all()
        self.fields['company'].required = True
        self.fields['company'].empty_label = None
    class Meta:
        model = User
        fields = ['company']


class ResetPasswordForm(forms.Form):

    email = forms.EmailField(label='E-mail utilizado')

    def save(self, user):
        return ResetPassword.objects.create(user=user)


class CheckResetPasswordForm(forms.Form):

    code = forms.CharField(label='Código')

    def __init__(self, reset_password, *args, **kwargs):
        self.reset_password = reset_password
        super().__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code and code != self.reset_password.code:
            raise forms.ValidationError('O código está incorreto!')
        return code
