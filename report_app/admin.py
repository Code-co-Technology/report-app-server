from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from report_app.models import Bob, TypeWork, Reports, RespostComment, ReportsName


class AdminRespostBob(admin.ModelAdmin):
    list_display = ['id', 'name']

admin.site.register(Bob, AdminRespostBob)


class AdminTypeWork(admin.ModelAdmin):
    list_display = ['id', 'name']

admin.site.register(TypeWork, AdminTypeWork)


class LimitInlineCommentFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # count all forms that have not been marked for deletion
        count = sum(1 for form in self.forms if not self._should_delete_form(form))
        max_num = 20  # specify your max number of images here
        if count > max_num:
            raise ValidationError(f'You can only associate up to {max_num} images with this product.')


class RepostCommentInline(admin.TabularInline):
    model = RespostComment
    formset = LimitInlineCommentFormSet
    extra = 1
    min_num = 1
    max_num = 20


class LimitInlineReportFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # count all forms that have not been marked for deletion
        count = sum(1 for form in self.forms if not self._should_delete_form(form))
        max_num = 50  # specify your max number of images here
        if count > max_num:
            raise ValidationError(f'You can only associate up to {max_num} images with this product.')


class RepostReportInline(admin.TabularInline):
    model = Reports
    formset = LimitInlineCommentFormSet
    extra = 1
    min_num = 1
    max_num = 50



class AdminReportsName(admin.ModelAdmin):
    inlines = [
        RepostReportInline,
        RepostCommentInline,
    ]
    list_display = ['id', 'name']
    search_fields = ['name']
    list_filter = ['name']

admin.site.register(ReportsName, AdminReportsName)