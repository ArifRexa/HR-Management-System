from django.contrib.auth.models import AnonymousUser
from django.db.models import Count, BooleanField, Case, When, Value, Min, Q, Prefetch
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from config.settings import employee_ids as management_ids

from employee.admin.employee.extra_url.formal_view import EmployeeNearbySummery
from employee.forms.employee_online import EmployeeStatusForm
from employee.forms.employee_project import EmployeeProjectForm
from employee.forms.employee_need_help import EmployeeNeedHelpForm
from employee.models import (
    EmployeeOnline,
    Leave,
    EmployeeSkill,
    HomeOffice,
    EmployeeNeedHelp,
    NeedHelpPosition,
    Employee
)
from employee.models.employee_activity import EmployeeProject
from employee.models.employee_feedback import EmployeeFeedback
from employee.models.employee import Employee, BookConferenceRoom
from employee.models import FavouriteMenu
from employee.forms.employee_project import BookConferenceRoomForm
from project_management.models import Project

from settings.models import Announcement

from datetime import datetime


def formal_summery(request):
    if not request.user.is_authenticated:
        return {}

    employee_id = request.user.employee.id

    employee_formal_summery = EmployeeNearbySummery()

    leaves_nearby, leaves_nearby_count = employee_formal_summery.employee_leave_nearby()
    permanents, permanents_count = employee_formal_summery.permanents()
    anniversaries, anniversaries_count = employee_formal_summery.anniversaries()

    employee_online = (
        EmployeeOnline.objects.filter(
            employee__active=True,
        )
        .order_by(
            "-employee__need_cto",
            "-employee__need_hr",
            "active",
            "employee__full_name",
        )
        .exclude(
            employee_id__in=management_ids,
        )
        .select_related(
            "employee",
        )
    )

    employee_projects = (
        EmployeeProject.objects.filter(
            employee__active=True,
            employee__project_eligibility=True,
        )
        .exclude(employee_id__in=management_ids)
        .annotate(
            project_count=Count("project"),
            project_order=Min("project"),
            project_exists=Case(
                When(project_count=0, then=Value(False)),
                default=Value(True),
                output_field=BooleanField(),
            ),
        )
        .order_by(
            "project_exists",
            "employee__full_name",
        )
        .select_related(
            "employee",
        )
        .prefetch_related(
            Prefetch(
                "employee__employeeskill_set",
                queryset=EmployeeSkill.objects.order_by("-percentage"),
            ),
            Prefetch("employee__employeeskill_set__skill"),
            Prefetch(
                "project",
                queryset=Project.objects.filter(active=True),
            ),
        )
    )

    order_keys = {
        "1": "employee__full_name",
        "-1": "-employee__full_name",
        "2": "project_order",
        "-2": "-project_order",
    }

    order_by = request.GET.get("ord", None)
    if order_by:
        order_by_list = ["project_exists", order_keys.get(order_by, "1")]
        if order_by not in ["1", "-1"]:
            order_by_list.append("employee__full_name")

        employee_projects = employee_projects.order_by(*order_by_list)

    current_month_feedback_done = True
    if str(employee_id) not in management_ids:
        current_month_feedback_done = EmployeeFeedback.objects.filter(
            employee_id=employee_id,
            created_at__date__month=timezone.now().date().month,
        ).exists()

    return {
        "leaves": leaves_nearby,
        "leaves_count": leaves_nearby_count,
        "employee_online": employee_online,
        "employee_projects": employee_projects,
        "ord": order_by,
        "current_month_feedback_done": current_month_feedback_done,
        "announcement": get_announcement(request=request),
        "birthday_today": get_managed_birthday_image(request),
        "increments": employee_formal_summery.increments,
        "permanents": permanents,
        "permanents_count": permanents_count,
        "anniversaries": anniversaries,
        "anniversaries_count": anniversaries_count,
        "is_management": str(employee_id) in management_ids,
        # TODO: Need Optimization
        "birthdays": employee_formal_summery.birthdays,
        "new_employees": employee_formal_summery.new_employee,
        "new_lead_or_managers": employee_formal_summery.new_lead_or_manager,
    }


def employee_status_form(request):
    if (
        request.user.is_authenticated
        and str(request.user.employee.id) not in management_ids
    ):
        employee_online = EmployeeOnline.objects.get(
            employee_id=request.user.employee.id
        )
        return {"status_form": EmployeeStatusForm(instance=employee_online)}
    else:
        return {"status_form": None}


def employee_project_form(request):
    if (
        request.user.is_authenticated
        and not str(request.user.employee.id) in management_ids
    ):
        employee_project = EmployeeProject.objects.get(
            employee_id=request.user.employee.id
        )
        return {"employee_project_form": EmployeeProjectForm(instance=employee_project)}
    else:
        return {"employee_project_form": None}


def employee_need_help_form(request):
    if (
        request.user.is_authenticated
        and not str(request.user.employee.id) in management_ids
    ):
        employee_need_help, _ = EmployeeNeedHelp.objects.get_or_create(
            employee_id=request.user.employee.id,
        )
        return {
            "employee_need_help_form": EmployeeNeedHelpForm(instance=employee_need_help)
        }
    else:
        return {"employee_need_help_form": None}


def get_announcement(request):
    data = []
    now = timezone.now()

    # Get Announcements
    announcements = (
        Announcement.objects.filter(
            is_active=True,
            start_datetime__lte=now,
            end_datetime__gte=now,
        )
        .order_by(
            "-updated_at",
            "-rank",
        )
        .values_list("description", flat=True)
    )

    need_help_positions = (
        NeedHelpPosition.objects.filter(
            employeeneedhelp__employee__active=True,
        )
        .distinct()
        .order_by("id")
    )
    for need_help_position in need_help_positions:
        title = need_help_position.title
        names = list(
            need_help_position.employeeneedhelp_set.values_list(
                "employee__full_name",
                flat=True,
            )
        )
        if names and (
            title != "CEO"
            or (
                title == "CEO"
                and request.user.employee.id == 30  # Employee ID must be 30
            )
        ):
            names_str = ", ".join(names)
            data.append(
                f"{names_str} need{'s' if len(names)==1 else ''} the {title}'s help."
            )

    # Announcements
    data.extend(announcements)

    # Get Leaves
    leaves_today = (
        Leave.objects.filter(
            employee__active=True,
            start_date__lte=now,
            end_date__gte=now,
        )
        .exclude(
            status="rejected",
        )
        .select_related(
            "employee",
        )
    )
    if leaves_today.exists():
        approved_leaves = Leave.objects.filter(status='Approved')
        count = approved_leaves.count()
        for i in range(0, count):
            today_date = datetime.now().date()
            if today_date == approved_leaves[i].start_date:
                data.extend([f"{approved_leaves[i].employee.full_name} is on {approved_leaves[i].leave_type} leave today."])

    # Get Home Offices
    home_offices_today = (
        HomeOffice.objects.filter(
            employee__active=True,
            start_date__lte=now,
            end_date__gte=now,
        )
        .exclude(
            status="rejected",
        )
        .select_related(
            "employee",
        )
    )
    if home_offices_today.exists():
        homeoffices = [
            homeoffice.employee.full_name for homeoffice in home_offices_today
        ]
        data.extend(
            [f"{homeoffice} is on Home Office today." for homeoffice in homeoffices]
        )

    # Get Birthdays
    birthdays_today = Employee.objects.filter(
        active=True,
        date_of_birth__day=now.date().day,
        date_of_birth__month=now.date().month,
    ).values_list("full_name", flat=True)
    if birthdays_today:
        birthdays_text = ", ".join(birthdays_today)
        data.append(
            f"{birthdays_text} {'has' if len(birthdays_today)==1 else 'have'} birthday today."
        )

    # Format Data
    if data:
        initial = f'<span style="background-color:tomato;padding:0.4rem 0.8rem;border-radius:0.4rem;">ANNOUNCEMENTS</span> {"&nbsp;"*8}🚨'
        data = initial + f' {"&nbsp;"*8}🚨'.join(
            [f'<span class="single_announcement">{d}</span>' for d in data]
        )
        data = format_html(data)

    return data if data else None


def get_managed_birthday_image(request):
    path = request.get_full_path()
    if not path == "/admin/":
        return False

    if isinstance(request.user, AnonymousUser):
        birthday = False
    else:
        birthday = False
        if request.user.employee.date_of_birth == datetime.today().date():
            if not request.user.employee.birthday_image_shown:
                try:
                    birthday = request.user.employee.birthday_image.url
                except:
                    birthday = False
                Employee.objects.filter(user=request.user).update(
                    birthday_image_shown=True
                )
            else:
                Employee.objects.filter(user=request.user).update(
                    birthday_image_shown=False
                )
    return birthday


def favourite_menu_list(request):
    if request.user.is_authenticated and request.user.employee is not None:
        f_menu = FavouriteMenu.objects.filter(employee_id=request.user.employee.id)
        data = {}
        data["object_list"] = f_menu
        return data
    return []
from project_management.models import Project
def project_lists(request):
    if request.user.is_authenticated:
        data = {}
        data['active_projects'] = Project.objects.filter(active=True)
        return data
    return []

def conference_room_bookings(request):
    today = datetime.today().date()
    return {'conference_room_bookings': BookConferenceRoom.objects.filter(created_at__date=today).order_by('start_time')}
    # return {'conference_room_bookings': BookConferenceRoom.objects.all()}

def conference_room_bookings_form(request):
    form = BookConferenceRoomForm
    
    # Return the form in a dictionary
    return {'my_form': form}

def employee_context_processor(request):
    if request.user.is_authenticated:
        try:
            employee = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            employee = None
        
        if employee:
            is_manager = employee.manager
            is_lead = employee.lead
            is_sqa = employee.sqa
            
        else:
            is_manager = False
            is_lead = False
            is_sqa = False
            
    else:
        employee = None
        is_manager = False
        is_lead = False
        is_sqa = False
        
    
    return {
        'employee': employee,
        'is_manager': is_manager,
        'is_lead': is_lead,
        'is_sqa': is_sqa,
        
    }


def employee_project_list(request):
    if request.user.is_authenticated:
        try:
            employee = Employee.objects.get(user=request.user)
            project_queryset = employee.employee_project_list.values_list('title', flat=True)
            project_list = list(project_queryset)
        except Employee.DoesNotExist:
            project_list = None
    else:
        project_list = None
    
    return {'employee_project_list': project_list}