from django.utils.timezone import now
from rest_framework import serializers
from phsw_site.base.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'cpf', 'fk_empresa', 'is_agente_admin', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            cpf=self.validated_data['cpf'],
            fk_empresa=self.validated_data['fk_empresa'],
            is_agente_admin=self.validated_data['is_agente_admin'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    days_since_joined = serializers.SerializerMethodField()
    empresa = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'cpf', 'is_agente_admin', 'empresa',
                  'days_since_joined']

    def get_days_since_joined(self, obj):
        return (now() - obj.date_joined).days

    def get_empresa(self, obj):
        return str(obj.fk_empresa)