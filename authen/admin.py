from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authen.models import CustomUser, Company, Overdue, FailedReports


admin.site.register(Overdue)
admin.site.register(FailedReports)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'activate_profile',]
    search_fields = ['email',]
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Personal Information', {'fields': ('phone', 'avatar', 'company', 'activate_profile', 'overdue', 'failed_reports', 'penalty', 'block_contractor', 'block_sending_report', 'report_processing', 'creating_prescriptions', 'processing_orders',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)


admin.site.register(Company)