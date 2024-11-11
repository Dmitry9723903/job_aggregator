from .models import User, Session
from rest_framework import serializers
import logging

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'created', "updated", 'is_active')

    def validate(self, attrs):
        """Общая валидация для атрибутов."""
        if 'email' not in attrs or 'password' not in attrs:
            logger.warning(f"Попытка регистрации с неверными атрибутами: email и пароль обязательны для заполнения.")
            raise serializers.ValidationError("Email и пароль обязательны для заполнения.")

        # Дополнительная проверка(если email уже существует)
        if User.objects.filter(email=attrs['email']).exists():
            logger.warning(f"Попытка регистрации с уже существующим email: {attrs['email']}")
            raise serializers.ValidationError("Этот email уже используется.")

        logger.info("Атрибуты прошли валидацию.")
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        """Проверка длины пароля."""
        if len(value) < 8:
            logger.warning(f"Попытка регистрации с коротким паролем: {len(value)} символов.")
            raise serializers.ValidationError("Пароль должен содержать не менее 8 символов.")
        logger.info("Пароль прошел валидацию.")
        return value


    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        logger.info(f"Создан новый пользователь: {validated_data['email']}")
        return user


# class SessionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Session
#         fields = '__all__'
