from django.contrib import admin
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from admin_account.models import CustomUser
from admin_account.models import ProjectStatus, Project, ProjectImage, ProjectSmeta


class AdminProjectStatus(admin.ModelAdmin):
    list_display = ['id', 'name']

admin.site.register(ProjectStatus, AdminProjectStatus)


class LimitInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # count all forms that have not been marked for deletion
        count = sum(1 for form in self.forms if not self._should_delete_form(form))
        max_num = 10  # specify your max number of images here
        if count > max_num:
            raise ValidationError(f'You can only associate up to {max_num} images with this product.')


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    formset = LimitInlineFormSet
    extra = 1
    min_num = 1
    max_num = 10


class ProjectFileInline(admin.TabularInline):
    model = ProjectSmeta
    formset = LimitInlineFormSet
    extra = 1
    min_num = 1
    max_num = 10


class AdminProject(admin.ModelAdmin):
    inlines = [
        ProjectImageInline,
        ProjectFileInline
    ]
    list_display = ['id', 'address', 'opening_date', 'submission_deadline', 'status']
    search_fields = ['id', 'address']
    list_filter = ['status']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'contractors':
            # "contractor" roligga ega foydalanuvchilarni ko'rsatish
            contractor_group = Group.objects.get(name="contractors")
            kwargs["queryset"] = CustomUser.objects.filter(groups=contractor_group)

        if db_field.name == 'owner':
            # "admin" roligga ega foydalanuvchilarni ko'rsatish
            admin_group = Group.objects.get(name="admin")
            kwargs["queryset"] = CustomUser.objects.filter(groups=admin_group)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Project, AdminProject)