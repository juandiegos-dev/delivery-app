from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from accesos.models import Usuario


class RegistroSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=100,
        trim_whitespace=False
    )

    class Meta:
        model = Usuario
        fields = [
            "id",
            "username",
            "email",
            "password",
            "rol"
        ]

    def validate(self, datos):
        usuario = Usuario(
            username=datos.get("username", ""),
            email=datos.get("email", "")
        )

        try:
            validate_password(
                datos["password"],
                user=usuario
            )
        except DjangoValidationError as error:
            raise serializers.ValidationError({
                "password": list(error.messages)
            })

        return datos

    def create(self, datos):
        return Usuario.objects.create_user(**datos)


class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = [
            "id",
            "username",
            "email",
            "rol"
        ]