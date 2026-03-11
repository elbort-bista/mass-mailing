from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SMTPConfiguration, EmailSettings, User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser', 'created_at')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

@admin.register(SMTPConfiguration)
class SMTPConfigurationAdmin(admin.ModelAdmin):
    list_display = ('smtp_host', 'smtp_port', 'smtp_username', 'is_active', 'updated_at')
    list_filter = ('is_active', 'smtp_use_tls', 'smtp_use_ssl', 'created_at')
    search_fields = ('smtp_host', 'smtp_username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('SMTP Server Configuration', {
            'fields': ('smtp_host', 'smtp_port', 'is_active')
        }),
        ('Authentication', {
            'fields': ('smtp_username', 'smtp_password')
        }),
        ('Connection Security', {
            'fields': ('smtp_use_tls', 'smtp_use_ssl')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_readonly_fields(self, request, obj=None):
        # Make password field readonly when editing existing objects
        if obj:
            return self.readonly_fields + ('smtp_password',)
        return self.readonly_fields

@admin.register(EmailSettings)
class EmailSettingsAdmin(admin.ModelAdmin):
    list_display = ('default_from_email', 'email_timeout', 'use_django_backend')
    fieldsets = (
        ('Default Email Settings', {
            'fields': ('default_from_email', 'email_timeout')
        }),
        ('Backend Configuration', {
            'fields': ('use_django_backend',)
        })
    )
