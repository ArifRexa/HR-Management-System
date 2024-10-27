import calendar
import datetime
import math
from dateutil.relativedelta import relativedelta, FR

from . models import EmployeeAttendance
from datetime import datetime
from django.core import management
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template import Context, loader
from django.template.loader import get_template
from django.utils import timezone
from django.conf import settings
from django.db.models import (
    Prefetch,
    F,
    ExpressionWrapper,
    FloatField,
    Q,
    Subquery,
    OuterRef,
)
from employee.models.employee import LateAttendanceFine
from employee.models import (
    Employee,
    Leave,
    LeaveManagement,
    EmployeeOnline,
    EmployeeAttendance,
    PrayerInfo,
    EmployeeFeedback,
    SalaryHistory,
    NeedHelpPosition,
    HRPolicy,
    EmployeeRating,
    
)
from project_management.models import (
    ProjectHour,
    EmployeeProjectHour,
    DailyProjectUpdate,
    Project,
)
from account.models import Loan


def set_default_exit_time():
    NOW = datetime.datetime.now()
    DEFAULT_EXIT_HOUR = 12 + 8  # 24 hour time == 9pm
    DEFAULT_EXIT_TIME = NOW.replace(hour=DEFAULT_EXIT_HOUR, minute=0, second=0)

    employee_onlines = EmployeeOnline.objects.filter(active=True)

    for emp_online in employee_onlines:
        attandance = emp_online.employee.employeeattendance_set.last()

        activities = attandance.employeeactivity_set.all()
        if activities.exists():
            activities = list(activities)
            start_time = activities[-1].start_time
            end_time = activities[-1].end_time
            if not end_time:
                if start_time.hour < DEFAULT_EXIT_HOUR:
                    activities[-1].end_time = DEFAULT_EXIT_TIME
                else:
                    activities[-1].end_time = start_time
                activities[-1].is_updated_by_bot = True
                activities[-1].save()


def send_mail_to_employee(employee, pdf, html_body, subject, letter_type):
    email = EmailMultiAlternatives()
    email.subject = f"{subject} of {employee.full_name}"
    email.attach_alternative(html_body, "text/html")
    email.to = [employee.email]
    email.from_email = '"Mediusware-Admin" <admin@mediusware.com>'
    email.attach_file(pdf)
    if letter_type == "EAL":
        hr_policy = HRPolicy.objects.last()
        file_path = hr_policy.policy_file.path
        if file_path:
            email.attach_file(file_path)
    email.send()


def leave_mail(leave: Leave):
    leave_manage = LeaveManagement.objects.filter(leave=leave)
    manager_email = []
    for leave_manage_obj in leave_manage:
        manager_email.append(leave_manage_obj.manager.email)
    email = EmailMessage()
    message_body = f"{leave.message} \n {leave.note} \n Status : {leave.status}"
    if leave.status == "pending":
        email.from_email = f"{leave.employee.full_name} <{leave.employee.email}>"
        email.to = ['"Mediusware-HR" <hr@mediusware.com>', 'shuyaib@mediusware.com']
        email.cc = manager_email
    else:
        email.from_email = '"Mediusware-HR" <hr@mediusware.com>'
        email.to = [f"{leave.employee.full_name} <{leave.employee.email}>"]
    email.subject = f"Leave application {leave.leave_type}, {leave.status}"
    email.body = message_body
    email.send()


# TODO : Resignation notification


def permanent_notification(employees):
    html_body = loader.render_to_string(
        "mails/permanent_notification.html",
        context={"employees": employees, "total_emp": len(employees)},
    )
    email = EmailMultiAlternatives()
    email.subject = f"Permanent Notification there are {len(employees)} employee in the list of permanent"
    email.attach_alternative(html_body, "text/html")
    email.to = ["admin@mediusware.com"]
    # email.bcc = ['coredeveloper.2013@gmail.com',]
    email.from_email = "no-reply@mediusware.com"
    email.send()


def increment_notification(employees):
    html_body = loader.render_to_string(
        "mails/increment_notification.html",
        context={"employees": employees, "total_emp": len(employees)},
    )
    email = EmailMultiAlternatives()
    email.subject = f"Increment Notification there are {len(employees)} employee(s) in the lis of increment"
    email.attach_alternative(html_body, "text/html")
    email.to = ["admin@mediusware.com"]
    # email.bcc = ['coredeveloper.2013@gmail.com',]
    email.from_email = "no-reply@mediusware.com"
    email.send()


def execute_increment_notification():
    management.call_command("increment_notifi")


def execute_permanent_notification():
    management.call_command("permanent_notifi")


def execute_birthday_notification():
    management.call_command("birthday_wish")


def no_daily_update():
    project_id = 92  # No Client Project - 92  # local No client Project id 2
    manager_employee_id = 30  # Shahinur Rahman - 30   # local manager id himel vai 9

    today = timezone.now().date()

    daily_update_emp_ids = (
        DailyProjectUpdate.objects.filter(created_at__date=today)
        .values_list("employee__id", flat=True)
        .distinct()
    )
    # emp_on_leave_today = Leave.objects.filter(status="approved", start_date__lte=today, end_date__gte=today).values_list('employee__id', flat=True)

    daily_update_eligibility = (
        Employee.objects.filter(active=True)
        .exclude(manager=True, lead=True)
        .exclude(project_eligibility=False)
    )

    missing_daily_update = (
        EmployeeAttendance.objects.filter(date=today)
        .filter(employee__id__in=daily_update_eligibility)
        .exclude(employee__id__in=daily_update_emp_ids)
    )

    if not missing_daily_update.exists():
        return

    if missing_daily_update.exists():
        emps = list()
        for employee in missing_daily_update:
            emps.append(
                DailyProjectUpdate(
                    employee_id=employee.employee_id,
                    manager_id=manager_employee_id,
                    project_id=project_id,
                    update="-",
                )
            )
        DailyProjectUpdate.objects.bulk_create(emps)

        # print("[Bot] Daily Update Done")


def no_project_update():
    today_date = timezone.now().date()
    today_day = today_date.strftime("%A")
    sat_or_sun_day = today_day == "Saturday" or today_day == "Sunday"
    # print(sat_or_sun_day)
    from_daily_update = (
        DailyProjectUpdate.objects.filter(
            project__active=True, created_at__date=today_date
        )
        .values_list("project__id", flat=True)
        .distinct()
    )

    if from_daily_update.exists() and not sat_or_sun_day:
        project_update_not_found = (
            Project.objects.filter(active=True)
            .exclude(id__in=from_daily_update)
            .distinct()
        )

        if not project_update_not_found.exists():
            return

        emp = Employee.objects.filter(
            id=30
        ).first()  # Shahinur Rahman - 30   # local manager id himel vai 9
        man = Employee.objects.filter(
            id=30
        ).first()  # Shahinur Rahman - 30   # local manager id himel vai 9

        if project_update_not_found.exists():
            punf = list()
            for no_upd_project in project_update_not_found:
                punf.append(
                    DailyProjectUpdate(
                        employee=emp,
                        manager=man,
                        project_id=no_upd_project.id,
                        update="-",
                    )
                )
            DailyProjectUpdate.objects.bulk_create(punf)
            # print("[Bot] No project update")
    return


def all_employee_offline():
    set_default_exit_time()
    # no_daily_update()
    # no_project_update()
    EmployeeOnline.objects.filter(active=True).update(active=False)


def bonus__project_hour__monthly(date, project_id, manager_employee_id):
    bonushour_for_feedback = 1

    employees = Employee.objects.filter(
        active=True,
        project_eligibility=True,
    ).prefetch_related(
        Prefetch(
            "employeefeedback_set",
            queryset=EmployeeFeedback.objects.filter(
                created_at__year=date.year,
                created_at__month=date.month,
            ),
        ),
    )

    project_hour = ProjectHour.objects.create(
        manager_id=manager_employee_id,
        hour_type="bonus",
        project_id=project_id,
        date=date,
        hours=0,
        description="Bonus for Monthly Feedback",
        # forcast = 'same',
        payable=True,
    )

    eph = []
    total_hour = 0

    for emp in employees:
        e_hour = 0

        if len(emp.employeefeedback_set.all()) > 0:
            e_hour += bonushour_for_feedback

        if e_hour > 0:
            total_hour += e_hour
            eph.append(
                EmployeeProjectHour(
                    project_hour=project_hour,
                    hours=e_hour,
                    employee=emp,
                )
            )

    project_hour.hours = total_hour
    project_hour.save()

    EmployeeProjectHour.objects.bulk_create(eph)
    print("[Bot] Monthly Bonus Done")


def bonus__project_hour_add(target_date=None):
    if not target_date:
        target_date = timezone.now().date()
    else:
        target_date = datetime.datetime.strptime(target_date, "%Y-%m-%d").date()

    project_id = 20  # HR - 20 # Local HR - 4
    manager_employee_id = 30  # Shahinur Rahman - 30 # Local ID - 1

    bonushour_for_timelyentry = 0
    bonushour_for_hroff = 0
    bonushour_for_overtime = 0
    bonushour_for_prayer = 0

    # Monthly bonus if it's the last day of the month
    _, last_day = calendar.monthrange(target_date.year, target_date.month)
    if target_date.day == last_day:
        bonus__project_hour__monthly(target_date, project_id, manager_employee_id)

    attendances = EmployeeAttendance.objects.filter(
        employee__active=True,
        employee__project_eligibility=True,
        date=target_date,
    ).prefetch_related(
        "employeeactivity_set",
        Prefetch(
            "employee",
            queryset=Employee.objects.select_related(
                "employeeonline",
            ).prefetch_related(
                Prefetch(
                    "prayerinfo_set",
                    queryset=PrayerInfo.objects.filter(created_at__date=target_date),
                ),
            ),
        ),
    )

    if len(attendances) > 0:
        # project_hour = ProjectHour.objects.create(
        #     manager_id = manager_employee_id,
        #     hour_type = 'bonus',
        #     project_id = project_id,
        #     date = target_date,
        #     hours = 0,
        #     description = 'Bonus for Entry / Exit / Exceeding 8 Hour / Prayer',
        #     # forcast = 'same',
        #     payable = True,
        # )

        eph = []
        total_hour = 0

        for attendance in attendances:
            if attendance.employeeactivity_set.exists():
                activities = list(attendance.employeeactivity_set.all())
                al = len(activities)

                e_hour = 0

                # If takes entry before 01:00 PM
                if al > 0 and activities[0].start_time.time() < datetime.time(
                    hour=13, minute=0, second=1
                ):
                    # print(attendance.employee.full_name, " - entry bonus")
                    e_hour += bonushour_for_timelyentry

                # Prayer Bonus
                if attendance.employee.prayerinfo_set.exists():
                    prayer_info = attendance.employee.prayerinfo_set.all()[0]
                    # print(attendance.employee.full_name, " - prayer bonus:", ((prayer_info.num_of_waqt_done // 2) * bonushour_for_prayer))
                    e_hour += (prayer_info.num_of_waqt_done // 2) * bonushour_for_prayer

                # If HR OFF for that date
                if (
                    al > 0
                    and activities[-1].end_time
                    and activities[-1].end_time.time()
                    < datetime.time(hour=23, minute=45, second=1)
                ):
                    # print(attendance.employee.full_name, " - hr off bonus")
                    e_hour += bonushour_for_hroff

                    inside_time = 0

                    for i in range(al):
                        st, et = activities[i].start_time, activities[i].end_time
                        if et:
                            inside_time += et.timestamp() - st.timestamp()

                    inside_time = math.floor(inside_time / 60)  # convert to minute

                    if inside_time >= 480:  # 8 hours = 480 minute
                        # print(attendance.employee.full_name, " - 8 hours bonus")
                        e_hour += bonushour_for_overtime

                total_hour += e_hour
                # eph.append(EmployeeProjectHour(
                #     project_hour = project_hour,
                #     hours = e_hour,
                #     employee=attendance.employee,
                # ))

        # project_hour.hours = total_hour
        # project_hour.save()

        # EmployeeProjectHour.objects.bulk_create(eph)
        print("[Bot] Bonus Done")


from employee.models import Employee, Config
from employee.mail import cto_help_mail, hr_help_mail, send_need_help_mails


def cto_help_pending_alert():
    current_time = timezone.now()

    # Send an email on office day every 2 hour.
    if current_time.weekday() > 4 or current_time.hour not in [12, 15, 18, 21]:
        return

    employees = Employee.objects.filter(need_cto=True)
    if Config.objects.first().cto_email is not None and employees is not None:
        email_list = Config.objects.first().cto_email.strip()
        email_list = email_list.split(",")

        for employee in employees:
            cto_help_mail(
                employee, {"waitting_at": employee.need_cto_at, "receiver": email_list}
            )


def hr_help_pending_alert():
    current_time = timezone.now()

    # Send an email on office day every 2 hour.
    if current_time.weekday() > 4 or current_time.hour not in [12, 15, 18, 21]:
        return

    employees = Employee.objects.filter(need_hr=True)
    if Config.objects.first().hr_email is not None and employees is not None:
        email_list = Config.objects.first().hr_email.strip()
        email_list = email_list.split(",")

        for employee in employees:
            hr_help_mail(
                employee, {"waiting_at": employee.need_hr_at, "receiver": email_list}
            )


def need_help_pending_alert():
    current_time = timezone.now()

    # Send an email on office day every 2 hour.
    if current_time.weekday() > 4 or current_time.hour not in [12, 14, 15, 18, 21]:
        return

    need_help_positions = NeedHelpPosition.objects.filter(active=True)
    for need_help_position in need_help_positions:
        employee_need_helps = need_help_position.employeeneedhelp_set.all()
        for employee_need_help in employee_need_helps:
            send_need_help_mails(employee_need_help)


def create_tds():
    today = timezone.now().date()
    recent_salary = (
        SalaryHistory.objects.filter(
            employee=OuterRef("pk"),
            active_from__lte=today,
        )
        .order_by("-active_from", "-id")
        .values("payable_salary")[:1]
    )

    employees = (
        Employee.objects.annotate(
            max_payable_salary=Subquery(recent_salary),
            counted_salary_amount=ExpressionWrapper(
                F("max_payable_salary") * (F("pay_scale__basic") / 100.0),
                output_field=FloatField(),
            ),
        )
        .filter(
            Q(active=True),
            Q(gender="male", counted_salary_amount__gte=25000.0)
            | Q(gender="female", counted_salary_amount__gte=28571.0),
        )
        .order_by("id")
    )

    LOAN_AMOUNT = 417
    LOAN_DATE = today + relativedelta(day=31)  # Gets the maximum month of that  day

    loans = list()
    for employee in employees:
        loans.append(
            Loan(
                employee=employee,
                witness_id=30,  # Must change  to 30
                loan_amount=LOAN_AMOUNT,
                emi=LOAN_AMOUNT,
                effective_date=LOAN_DATE,
                start_date=LOAN_DATE,
                end_date=LOAN_DATE,
                tenor=1,
                payment_method="salary",
                loan_type="tds",
            )
        )
    Loan.objects.bulk_create(loans)


# onetime call function for creating all entry_pass_id
def save_entry_pass_id():
    all_employees = Employee.objects.all()
    for employee in all_employees:
        employee.entry_pass_id = (
            f"{employee.joining_date.strftime('%Y%d')}{employee.id}"
        )
        employee.save()
    print("All Saved.")



def employee_attendance_old_data_delete(months):
    current_date = datetime.now()
    months_ago = relativedelta(months=months)

    target_date = current_date - months_ago
    old_data = EmployeeAttendance.objects.filter(created_at__lt=target_date)
    
    old_data.delete()

from datetime import datetime, time
from django.db.models.functions import ExtractMonth, ExtractYear

def late_attendance_calculate():
    employees = Employee.objects.filter(active=True).exclude(salaryhistory__isnull=True)
    late_entry = time(hour=11, minute=30)

    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    start_date = current_date.replace(day=1)
    end_date = current_date

    for employee in employees:
        total_late_entry = EmployeeAttendance.objects.filter(
            employee=employee,
            date__range=(start_date, end_date),
            entry_time__gt=late_entry
        ).count()
      
        if total_late_entry > 3:
            total_fine = (total_late_entry - 3) * 80  
        else:
            total_fine = 0.0

        # Update or create the LateAttendanceFine entry
        LateAttendanceFine.objects.update_or_create(
            employee=employee,
            month=current_month,
            year=current_year,
            defaults={'total_late_attendance_fine': total_fine}
        )