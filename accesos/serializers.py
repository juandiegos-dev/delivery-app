from rest_framework import serializers

from accesos.models import Usuario


class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, max_length=100)

    class Meta:
        model = Usuario
        fields = ["id", "username", "email", "password", "rol"]

    def create(self, datos):
        return Usuario.objects.create_user(**datos)


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "username", "email", "rol"]