from django.contrib import admin, messages

from employee.models import EmployeeNeedHelp, NeedHelpPosition


@admin.register(NeedHelpPosition)
class NeedHelpPositionAdmin(admin.ModelAdmin):
    search_fields = (
        "title",
        "email",
    )

    def has_module_permission(self, request):
        return False


# @admin.register(EmployeeNeedHelp)
# class EmployeeNeedHelpAdmin(admin.ModelAdmin):
#     list_display = (
#         "employee",
#         # "need_help_position",
#         # "active",
#     )
#     autocomplete_fields = (
#         "employee",
#         "need_help_position",
#     )
