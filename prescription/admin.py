from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from prescription.models import TypeOfViolation, Prescriptions, PrescriptionsImage, PrescriptionsComment, PrescriptionContractor



class LimitInlineContractorFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # count all forms that have not been marked for deletion
        count = sum(1 for form in self.forms if not self._should_delete_form(form))
        max_num = 30  # specify your max number of images here
        if count > max_num:
            raise ValidationError(f'You can only associate up to {max_num} images with this product.')


class ContractorInline(admin.TabularInline):
    model = PrescriptionContractor
    formset = LimitInlineContractorFormSet
    extra = 1
    min_num = 1
    max_num = 30



class AdminTypeOfViolation(admin.ModelAdmin):
    list_display = ['id', 'name']

admin.site.register(TypeOfViolation, AdminTypeOfViolation)


class LimitInlineImageFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # count all forms that have not been marked for deletion
        count = sum(1 for form in self.forms if not self._should_delete_form(form))
        max_num = 10  # specify your max number of images here
        if count > max_num:
            raise ValidationError(f'You can only associate up to {max_num} images with this product.')


class ImageInline(admin.TabularInline):
    model = PrescriptionsImage
    formset = LimitInlineImageFormSet
    extra = 1
    min_num = 1
    max_num = 10


class LimitInlineCommentFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # count all forms that have not been marked for deletion
        count = sum(1 for form in self.forms if not self._should_delete_form(form))
        max_num = 50  # specify your max number of images here
        if count > max_num:
            raise ValidationError(f'You can only associate up to {max_num} images with this product.')


class CommentInline(admin.TabularInline):
    model = PrescriptionsComment
    formset = LimitInlineCommentFormSet
    extra = 1
    min_num = 1
    max_num = 50


class AdminPrescriptions(admin.ModelAdmin):
    inlines = [
        ImageInline,
        CommentInline,
        ContractorInline,
    ]
    list_display = ['id', 'project']
    search_fields = ['project']
    list_filter = ['project']

admin.site.register(Prescriptions, AdminPrescriptions)