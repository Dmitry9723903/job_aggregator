from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from django.db.models.functions import Lower


class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """

    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        """Create and return a `User` with an email, phone number, username and password."""
        if email is None:
            raise TypeError("Users must have an email.")

        user = self.model(email=self.normalize_email(email.lower()))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError("Superusers must have a password.")
        if email is None:
            raise TypeError("Superusers must have an email.")

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=150, default="", blank=True)
    last_name = models.CharField(max_length=150, default="", blank=True)
    email = LowercaseEmailField(db_index=True, unique=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_subscribed = models.BooleanField(default=False)

    options = models.JSONField(null=True, blank=True)

    referral_code = models.CharField(max_length=150, blank=True, null=True, unique=True)
    referred_by = models.ForeignKey(
        "User", on_delete=models.SET_NULL, blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-is_active", Lower("email")]

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._groups = None

    def __str__(self):
        return f"{'💡' if self.is_active else '⭕'}{self.email}"

    @property
    def settings(self):
        if not self.options:
            self.options = {}
        return self.options

    @property
    def group_list(self):
        if self._groups is None:
            self._groups = self.groups.values_list("name", flat=True)
        return self._groups

    @settings.setter
    def settings(self, value):
        if isinstance(value, dict):
            self.options = dict(self.settings)
            self.options.update(value)


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()


class Role(models.Model):
    role_name = models.CharField(max_length=255)


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')


class Permission(models.Model):
    permission_name = models.CharField(max_length=255)


class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'permission')
