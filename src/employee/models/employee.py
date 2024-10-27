import datetime
from datetime import date as dt_date, time, datetime, timedelta
import uuid
import math
from django.contrib.auth.models import Group, User
from django.db import models
from django.db.models import Sum, Count, Avg
from django.db.models.functions import Coalesce, TruncMonth, ExtractMonth
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.html import format_html
from django.utils.text import slugify
from django.utils.timesince import timesince
from tinymce.models import HTMLField
from config.model.AuthorMixin import AuthorMixin
from config.model.TimeStampMixin import TimeStampMixin
from settings.models import Designation, LeaveManagement, PayScale
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from django.utils import timezone
# from project_management.models import Project


class Appointment(AuthorMixin, TimeStampMixin):
    is_completed = models.BooleanField(default=False)
    subject = models.CharField(max_length=255, blank=True, null=True)
    project = models.ForeignKey(
        "project_management.Project", null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"


class Employee(TimeStampMixin, AuthorMixin):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    full_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, null=True, blank=True, unique=True)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        null=True,
        blank=False,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True)
    address = models.TextField(verbose_name="Permanent Address", null=True)
    present_address = models.TextField(verbose_name="Present Address", null=True)
    phone = models.CharField(
        max_length=60, help_text="Use (,) comma for separate phone numbers"
    )
    joining_date = models.DateField(default=timezone.now)
    national_id_no = models.CharField(max_length=20, blank=True, null=True)
    permanent_date = models.DateField(null=True, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.RESTRICT)
    leave_management = models.ForeignKey(LeaveManagement, on_delete=models.RESTRICT)
    pay_scale = models.ForeignKey(PayScale, on_delete=models.RESTRICT)
    tax_info = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="i.e: 59530389237, Circle–138, Zone-11, Dhaka",
    )
    tax_eligible = models.BooleanField(default=True)
    manager = models.BooleanField(default=False)
    lead = models.BooleanField(default=False)
    sqa = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    show_in_web = models.BooleanField(default=True)
    operation = models.BooleanField(default=False)
    lunch_allowance = models.BooleanField(default=True)
    project_eligibility = models.BooleanField(default=True)
    leave_in_cash_eligibility = models.BooleanField(default=True)
    show_in_attendance_list = models.BooleanField(default=True)
    pf_eligibility = models.BooleanField(default=False)
    festival_bonus_eligibility = models.BooleanField(default=True)
    device_allowance = models.BooleanField(default=False)
    list_order = models.IntegerField(default=100)
    birthday_image = models.ImageField(null=True, blank=True)
    birthday_image_shown = models.BooleanField(default=False)
    need_cto = models.BooleanField(
        verbose_name="I need help from Tech Lead", default=False
    )
    need_cto_at = models.DateTimeField(null=True, blank=True)
    need_hr = models.BooleanField(verbose_name="I need help from HR", default=False)
    need_hr_at = models.DateTimeField(null=True, blank=True)
    entry_pass_id = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.full_name

    @property
    def has_pending_appointment(self):
        return Appointment.objects.filter(
            created_by=self.user, is_completed=False
        ).exists()

    @property
    def last_pending_appointment(self):
        return Appointment.objects.filter(
            created_by=self.user, is_completed=False
        ).first()

    @property
    def average_rating(self):
        four_months_ago = datetime.datetime.now() - datetime.timedelta(days=4 * 120)
        employee_ratings = self.employeerating_set.filter(
            created_at__gte=four_months_ago
        )
        return (
            employee_ratings.annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(avg_score=Avg("score"))
            .values("month", "avg_score")
        )

    @property
    def top_skills(self):
        skills = self.employeeskill_set.order_by("-percentage").all()
        return skills[:4]

    @property
    def is_online(self):
        from employee.models.employee_activity import EmployeeOnline

        return (
            EmployeeOnline.objects.filter(employee__active=True, employee__id=self.id)
            .values_list("active", flat=True)
            .first()
        )

    @property
    def employee_project_list(self):
        from employee.models.employee_activity import EmployeeProject

        return (
            EmployeeProject.objects.filter(employee_id=self.id)
            .first()
            .project.filter(active=True)
            .values("title")
        )

    @property
    def top_one_skill(self):
        return self.employeeskill_set.order_by("-percentage").first()

    @property
    def default_bank(self):
        bank = self.bankaccount_set.filter(default=True).first()
        if bank:
            return bank.bank.name
        return ""

    @property
    def one_month_less(self):
        current_month = datetime.today()
        emp_month = self.created_at - relativedelta(months=-1)
        if current_month < emp_month:
            return True
        return False

    @property
    def last_x_months_feedback(self):
        current_month = datetime.today()
        last_x_months = current_month + relativedelta(months=-6)
        return (
            self.employeefeedback_set.filter(
                created_at__lte=current_month,
                created_at__gte=last_x_months,
            )
            .order_by("-created_at")
            .exclude(employee__active=False)
        )

    @property
    def last_four_month_project_hours(self):
        # Employee Project Hour
        project_hours = (
            self.employeeprojecthour_set.filter(
                project_hour__date__gte=timezone.now() - relativedelta(months=3),
                project_hour__hour_type="project",
            )
            .annotate(month=TruncMonth("project_hour__date"))
            .values("month")
            .annotate(total_hours=Sum("hours"))
            .values("month", "total_hours")
        )

        # Manager Project Hour (Weekly Ones)
        manager_project_hours = (
            self.projecthour_set.filter(
                date__gte=timezone.now() - relativedelta(months=3),
                hour_type="project",
            )
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(
                total_hours=Coalesce(Sum("hours"), 0.0),
            )
            .values("month", "total_hours")
        )

        # Generate 4 months first day
        now = timezone.now().date().replace(day=1)
        last_x_months = [(now - relativedelta(months=i)) for i in range(4)]

        # Empty list for storing 4 months hour
        project_hour_list = []

        # Iterate through months and store the hours
        for month_date in last_x_months:
            temp_hours = 0.0

            # Employee Hour
            for hours in project_hours:
                month = hours["month"].replace(day=1)
                if month == month_date:
                    temp_hours += hours["total_hours"]
                    break

            # Manager Hour
            if manager_project_hours.exists():
                for manager_project_hour in manager_project_hours:
                    if month_date == manager_project_hour["month"].replace(day=1):
                        temp_hours += manager_project_hour["total_hours"]
                        break

            project_hour_list.append(temp_hours)

        format_str = "<hr>" + (
            " - ".join(
                map(
                    lambda x: f"{x:.2f}" if x != int(x) else f"{x:.1f}",
                    project_hour_list,
                )
            )
        )
        return format_html(format_str)

    @property
    def get_entry_pass_id(self):
        return f"{self.joining_date.strftime('%Y%d')}{self.id}"

    def save(
        self,
        *args,
        **kwargs,
    ):
        self.save_user()
        if not self.slug:
            self.slug = f"{slugify(self.full_name)}-{self.email}"[:180]
        # if not self.entry_pass_id:
        #     self.entry_pass_id = f"{self.joining_date.strftime('%Y%d')}{self.id}"
        super().save(*args, **kwargs)

    def save_user(self):
        name_array = self.full_name.split()
        self.user.is_staff = True
        self.user.first_name = name_array[0]
        self.user.last_name = name_array[1] if len(name_array) > 1 else ""
        self.user.email = self.email
        self.set_in_employee_group()
        if not self.active:
            self.user.is_active = False
        self.user.save()

    def set_in_employee_group(self):
        group = Group.objects.get(name="Employee")
        group.user_set.add(self.user)

    @property
    def joining_date_human(self):
        return timesince(self.joining_date)

    @property
    def permanent_date_human(self):
        return timesince(self.permanent_date)

    def approved_resignation(self):
        return self.resignation_set.filter(status="approved").first()

    @property
    def resignation_date(self):
        is_resigned = self.resignation_set.filter(status="approved").first()
        if is_resigned:
            return is_resigned.date
        return None

    @property
    def current_salary(self):
        return self.salaryhistory_set.latest("id")

    @property
    def joining_salary(self):
        return self.salaryhistory_set.first()

    @property
    def permanent_salary(self):
        salary = self.salaryhistory_set.filter(active_from=self.permanent_date).first()
        if salary:
            return salary
        return self.current_salary

    def set_daily_hours(self, value):
        self.daily_project_hours = value

    def set_employee_hours(self, value):
        self.employee_hours = value

    def leave_passed(self, leave_type: str, year=timezone.datetime.now().year):
        half_day_leaves = 0.0
        if leave_type == "casual":
            # Half day will be counted as half casual
            half_day_leaves = (
                self.leave_set.filter(
                    end_date__year=year,
                    leave_type="half_day",
                    status="approved",
                ).aggregate(total=Coalesce(Sum("total_leave"), 0.0))["total"]
                * 0.5
            )

        leaves_taken = self.leave_set.filter(
            end_date__year=year,
            leave_type=leave_type,
            status="approved",
        ).aggregate(total=Coalesce(Sum("total_leave"), 0.0))["total"]

        return half_day_leaves + leaves_taken

    def leave_available_leaveincash(
        self, leave_type: str, year_end=timezone.now().replace(month=12, day=31).date()
    ):
        available_leave = 0
        get_leave_by_type = getattr(self.leave_management, leave_type)

        if self.leave_in_cash_eligibility and self.permanent_date:
            if self.resignation_date:
                total_days_of_permanent = (
                    self.resignation_date - self.joining_date
                ).days
            else:
                total_days_of_permanent = (year_end - self.joining_date).days

            month_of_permanent = round(total_days_of_permanent / 30)
            if month_of_permanent < 12:
                available_leave = (month_of_permanent * get_leave_by_type) / 12
            else:
                available_leave = get_leave_by_type

        return round(available_leave)

    def leave_available(
        self, leave_type: str, year_end=timezone.now().replace(month=12, day=31).date()
    ):
        available_leave = 0
        get_leave_by_type = getattr(self.leave_management, leave_type)

        # Renamed for leave calculation
        # TODO: Need to upgrade calculation style without temporary fix
        permanent_date = self.joining_date
        current_year = timezone.now().year
        first_day_of_current_year = dt_date(current_year, 1, 1)

        if self.leave_in_cash_eligibility:
            if self.resignation_date:
                if self.joining_date < first_day_of_current_year:
                    total_days_of_permanent = (
                        self.resignation_date - first_day_of_current_year
                    ).days
                else:
                    total_days_of_permanent = (
                        self.resignation_date - self.joining_date
                    ).days

            else:
                if self.joining_date < first_day_of_current_year:
                    total_days_of_permanent = 365
                else:
                    total_days_of_permanent = (year_end - self.joining_date).days

            month_of_permanent = math.floor(total_days_of_permanent / 30)
            available_leave = (month_of_permanent * get_leave_by_type) / 12

        decimal_number = available_leave - int(available_leave)
        if decimal_number < 0.50:
            return float("{:.2f}".format(round(available_leave)))
        else:
            integer_part = math.floor(available_leave)
            available_leave = integer_part + 0.50
            return available_leave

    class Meta:
        db_table = "employees"
        permissions = (
            ("can_see_formal_summery_view", "Can able to see emloyee summary view"),
            ("can_access_all_employee", "Can acccess all employee"),
            ("can_access_average_rating", "Can access average rating of Employee."),
            ("can_see_salary_history", "Can able to see salary history."),
        )
        ordering = ["full_name"]


class BookConferenceRoom(models.Model):
    TIME_CHOICES = [
        # (time(hour, minute), f"{hour:02}:{minute:02}")
        (
            time(hour, minute),
            f"{(hour + 11) % 12 + 1}:{minute:02} {'AM' if hour < 12 else 'PM'}",
        )
        for hour in range(11, 21)
        for minute in (0, 30)
        if not (hour == 20 and minute == 30)
    ]

    manager_or_lead = models.ForeignKey("employee.Employee", on_delete=models.CASCADE)
    project_name = models.ForeignKey(
        "project_management.Project", on_delete=models.CASCADE
    )
    start_time = models.TimeField(choices=TIME_CHOICES)
    # end_time = models.TimeField(editable=False,)
    created_at = models.DateTimeField(default=timezone.now)  # Add created_at field

    def clean(self):
        # Check if there is any booking with overlapping time
        if self.pk:
            existing_bookings = BookConferenceRoom.objects.exclude(pk=self.pk).filter(
                start_time=self.start_time, created_at__date=timezone.now().date()
            )
        else:
            existing_bookings = BookConferenceRoom.objects.filter(
                start_time=self.start_time, created_at__date=timezone.now().date()
            )

        if existing_bookings.exists():
            raise ValidationError(
                f"Another conference room is already booked at this time.{self.start_time}"
            )

    @property
    def end_time(self):
        start_time = self.start_time
        end_time = datetime.combine(
            timezone.now().date(), start_time
        ) + timezone.timedelta(minutes=30)
        return end_time.time()

    def __str__(self):
        return f"Booking for {self.project_name} by {self.manager_or_lead.full_name} from {self.start_time}"


@receiver(post_save, sender=Employee, dispatch_uid="create_employee_lunch")
def create_employee_lunch(sender, instance, **kwargs):
    if instance.pf_eligibility:
        now = timezone.now().date().replace(day=1)
        maturity_date = now + relativedelta(years=2)
        from provident_fund.models import Account

        Account.objects.get_or_create(
            employee=instance,
            defaults={
                "start_date": now,
                "maturity_date": maturity_date,
                "scale": 10.0,
            },
        )

    from employee.models.employee_activity import EmployeeOnline, EmployeeProject

    EmployeeLunch.objects.update_or_create(employee=instance)
    EmployeeOnline.objects.get_or_create(employee=instance)
    EmployeeProject.objects.update_or_create(employee=instance)

    if kwargs.get("created"):
        # if not instance.entry_pass_id:
        instance.entry_pass_id = (
            f"{instance.joining_date.strftime('%Y%d')}{instance.id}"
        )
        instance.save()


class EmployeeLunch(TimeStampMixin):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    class Meta:
        permissions = (("can_see_all_lunch", "Can able to see all lunch"),)
        verbose_name = "Employee List"
        verbose_name_plural = "Employee List"


class PrayerInfo(AuthorMixin, TimeStampMixin):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    num_of_waqt_done = models.IntegerField(default=0)

    waqt_fajr = models.BooleanField(default=False)
    waqt_zuhr = models.BooleanField(default=False)
    waqt_asr = models.BooleanField(default=False)
    waqt_maghrib = models.BooleanField(default=False)
    waqt_isha = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.num_of_waqt_done = (
            self.waqt_fajr
            + self.waqt_zuhr
            + self.waqt_asr
            + self.waqt_maghrib
            + self.waqt_isha
        )

        return super(PrayerInfo, self).save(*args, **kwargs)


class Task(TimeStampMixin, AuthorMixin):
    is_complete = models.BooleanField(default=False)
    title = models.CharField(max_length=200, null=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Todo"
        verbose_name_plural = "Todo List"


class EmployeeFaq(TimeStampMixin, AuthorMixin):
    question = models.CharField(max_length=200)
    answer = HTMLField()
    rank = models.IntegerField(default=0)
    active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.question

    class Meta:
        permissions = (("can_approve_faq", "Can approve FAQ"),)

        verbose_name = "Set FAQ"
        verbose_name_plural = "Set FAQ"


class EmployeeFAQView(EmployeeFaq):
    class Meta:
        proxy = True
        verbose_name = "FAQ List"
        permissions = (("employee_faqs_view", "Can Employee FAQ list view."),)
        verbose_name_plural = "FAQ List"


class EmployeeNOC(TimeStampMixin, AuthorMixin):
    employee = models.OneToOneField(
        to=Employee,
        on_delete=models.CASCADE,
        limit_choices_to={"active": True},
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    noc_body = HTMLField()
    noc_pdf = models.FileField(upload_to="noc/", null=True, blank=True)
    noc_image = models.ImageField(upload_to="noc_images/", null=True, blank=True)


class Observation(TimeStampMixin, AuthorMixin):
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, related_name="observations"
    )

    class Meta:
        verbose_name = "Observe New Lead/Managers or New Dev"
        unique_together = ("employee",)
        # verbose_name_plural = 'Observations'



class LateAttendanceFine(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    total_late_attendance_fine = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=datetime.now,null=True,blank=True)

    class Meta:
        unique_together = ('employee', 'month', 'year')
    
    def __str__(self):
        return f"{self.employee.user.username} - {self.month}/{self.year}"