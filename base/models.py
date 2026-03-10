from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

class SMTPConfiguration(models.Model):
    smtp_host = models.CharField(max_length=255, default='smtp.gmail.com', help_text='SMTP server hostname')
    smtp_port = models.IntegerField(default=587, help_text='SMTP server port (587 for TLS, 465 for SSL)')
    smtp_username = models.CharField(max_length=255, help_text='SMTP username/email')
    smtp_password = models.CharField(max_length=255, help_text='SMTP password')
    smtp_use_tls = models.BooleanField(default=True, help_text='Use TLS encryption')
    smtp_use_ssl = models.BooleanField(default=False, help_text='Use SSL encryption')
    is_active = models.BooleanField(default=True, help_text='Use this configuration')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'SMTP Configuration'
        verbose_name_plural = 'SMTP Configurations'
    
    def __str__(self):
        return f"{self.smtp_host}:{self.smtp_port} - {self.smtp_username}"
    
    def save(self, *args, **kwargs):
        # Ensure only one configuration is active at a time
        if self.is_active:
            SMTPConfiguration.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

class EmailSettings(models.Model):
    default_from_email = models.EmailField(max_length=255, default='haripriyamax1427@gmail.com', help_text='Default from email address')
    email_timeout = models.IntegerField(default=30, help_text='Email timeout in seconds')
    use_django_backend = models.BooleanField(default=True, help_text='Use Django email backend as fallback')
    
    class Meta:
        verbose_name = 'Email Settings'
        verbose_name_plural = 'Email Settings'
    
    def __str__(self):
        return self.default_from_email
