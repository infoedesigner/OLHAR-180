import re

from rolepermissions.roles import assign_role

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User


class LoginSMSSerializer(serializers.Serializer):

    phone = serializers.CharField()

    def validae_phone(self, value):
        return re.sub(r'[\.-]', '', value)

class CheckSMSSerializer(LoginSMSSerializer):

    code = serializers.CharField()


class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key

    def validae_phone(self, value):
        if User.objects.filter(identifier=value).exists():
            raise serializers.ValidationError('Já exise usuário cadastrado com esse celular')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.identifier = user.phone
        user.save()
        assign_role(user, 'holder')
        return user

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'email', 'last_name', 'phone', 'password', 'token',
        ]
        read_only_fields = ['token']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'email', 'identifier', 'county', 'phone', 'created',
            'modified', 'is_staff', 'is_superuser', 'active'
        ]
        read_only_fields = [
            'is_staff', 'is_superuser', 'last_access', 'created', 'modified', 'identifier'
        ]


class PasswordChangeSerializer(serializers.Serializer):

    old_password = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Senha atual inválida, favor informar a senha atual')
        return value

    def validate(self, data):
        password = data['password']
        confirm_password = data['confirm_password']
        if password != confirm_password:
            raise serializers.ValidationError({'confirm_password': 'A confirmação da senha não confere'})
        return data

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['password'])
        user.save()
        return user
