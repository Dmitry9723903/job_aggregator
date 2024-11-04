import logging
import json

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()


class Subscription(models.Model):
    SERVICE_TOKENS = (
        ("system", "System"),
        ("bot", "Bot"),
    )

    service = models.CharField(
        "Сервис", max_length=10, choices=SERVICE_TOKENS, db_index=True
    )
    name = models.CharField("Название", max_length=200)

    price = models.DecimalField("Цена", max_digits=20, decimal_places=2, null=True)
    params = models.TextField(
        "Настройки", null=True, blank=True, default='{"shops": 3, "type": "primary"}'
    )
    start_at = models.DateField("Начало действия", default=timezone.now)
    stop_at = models.DateField("Конец действия", default=timezone.now)

    is_active = models.BooleanField("Включена", default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = [
            "-is_active",
            "stop_at",
        ]

    @property
    def params_json(self):
        if not self.params:
            return {}

        try:
            params = json.loads(self.params.replace("'", '"'))
        except json.decoder.JSONDecodeError:
            params = {}

        if type(params) is not dict:
            params = {}
        return params

    @property
    def is_alive(self):
        return self.is_active and self.start_at <= timezone.now().date() <= self.stop_at

    @property
    def before_stop(self):
        if self.is_alive:
            return (self.stop_at - timezone.now().date()).days
        else:
            return None

    def __str__(self):
        if self.pk:
            name = (
                f"✅ {self.service.upper()}.{self.name} ({self.before_stop} дн)"
                if self.is_alive
                else f"⭕ Неактивна"
            )
        else:
            name = f"⭕ Отсутствует"
        return name
