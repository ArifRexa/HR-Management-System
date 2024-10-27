from django.contrib import admin
from django.db import models
from django.forms import Textarea

from employee.models import (
    SalaryHistory,
    Attachment,
    BankAccount,
    EmployeeSkill,
    EmployeeSocial,
    EmployeeContent,
    EmployeeNOC,
)


class SalaryHistoryInline(admin.TabularInline):
    model = SalaryHistory

    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 2, "cols": 60})}
    }

    def get_extra(self, request, obj=None, **kwargs):
        return 1 if not obj else 0

    def get_fields(self, request, obj=None):
        fields = super(SalaryHistoryInline, self).get_fields(request, obj)
        if not request.user.is_superuser:
            fields.remove("note")
        return fields


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0


class BankAccountInline(admin.TabularInline):
    model = BankAccount

    def get_extra(self, request, obj=None, **kwargs):
        return 1 if not obj else 0


class SkillInline(admin.TabularInline):
    model = EmployeeSkill
    autocomplete_fields = ["skill"]

    def get_extra(self, request, obj=None, **kwargs):
        return 1 if not obj else 0


class EmployeeSocialInline(admin.TabularInline):
    model = EmployeeSocial
    extra = 0


class EmployeeContentInline(admin.StackedInline):
    model = EmployeeContent
    extra = 0


class EmployeeNOCInlineAdmin(admin.StackedInline):
    model = EmployeeNOC
    readonly_fields = ("uuid", "noc_pdf")
    extra = 0

    def get_fields(self, request, obj=None):
        fields: list = super().get_fields(request, obj)
        if (
            getattr(obj, "employeenoc", None)
            and obj.employeenoc.noc_pdf
            and "noc_body" in fields
        ):
            pass
            # fields.remove("noc_body")
        return fields


class EmployeeInline(admin.ModelAdmin):
    inlines = (
        SkillInline,
        AttachmentInline,
        SalaryHistoryInline,
        BankAccountInline,
        EmployeeSocialInline,
        EmployeeContentInline,
        EmployeeNOCInlineAdmin,
    )

    def get_inline_instances(self, request, obj):
        inlines = super().get_inline_instances(request, obj)
        if (
            not request.user.is_superuser
            and obj
            and request.user != obj.user
            and self.has_module_permission
        ):
            for inline_obj in inlines.copy():
                if isinstance(inline_obj, SalaryHistoryInline):
                    inlines.remove(inline_obj)
        return inlines
