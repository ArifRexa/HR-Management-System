from datetime import datetime
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta, FR
from uuid import uuid4

from django.utils import timezone
from datetime import date
from dateutil.utils import today
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum, ExpressionWrapper, Case, Value, When, F, Q
from django.db.models.functions import Trunc, ExtractWeekDay, ExtractWeek
from django.db.models.signals import pre_save
from django.db.models.signals import post_save

from django.dispatch import receiver
from tinymce.models import HTMLField
from config.model.TimeStampMixin import TimeStampMixin
from config.model.AuthorMixin import AuthorMixin
from employee.models import Employee
from django.utils.html import format_html

from icecream import ic
# from employee.models import LeaveManagement
from django.apps import apps



class Technology(TimeStampMixin, AuthorMixin):
    icon = models.ImageField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Tag(TimeStampMixin, AuthorMixin):
    icon = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name




class Client(TimeStampMixin, AuthorMixin):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(max_length=80)
    cc_email = models.TextField(null=True, blank=True, help_text="Comma-separated email addresses for CC")
    address = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=200)
    logo = models.ImageField(null=True, blank=True)
    # show_in_web = models.BooleanField(default=False)
    client_feedback = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="client_images", null=True, blank=True)

    def __str__(self):
        return self.name

class ProjectOverview(TimeStampMixin, AuthorMixin):
    title = models.CharField(max_length=100)
    description = HTMLField()
    img = models.ImageField()

    def __str__(self):
        return self.title

class ProjectStatement(TimeStampMixin, AuthorMixin):
    title = models.CharField(max_length=100)
    description = HTMLField()
    img = models.ImageField()

    def __str__(self):
        return self.title

class ProjectChallenges(TimeStampMixin, AuthorMixin):
    title = models.CharField(max_length=100)
    description = HTMLField()
    img = models.ImageField()

    def __str__(self):
        return self.title

class ProjectSolution(TimeStampMixin, AuthorMixin):
    title = models.CharField(max_length=100)
    description = HTMLField()
    img = models.ImageField()

    def __str__(self):
        return self.title

from django.db import models





class ProjectResults(models.Model):
    title = models.CharField(max_length=200)
    increased_sales = models.CharField(max_length=20) 
    return_on_investment = models.CharField(max_length=10)  
    increased_order_rate = models.CharField(max_length=20) 

    def __str__(self):
        return self.title
    

class ProjectPlatform(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class ProjectIndustry(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
class ProjectService(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
# Create your models here.
class Project(TimeStampMixin, AuthorMixin):
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True, unique=True)
    description = models.TextField()
    client = models.ForeignKey(
        Client, on_delete=models.SET_NULL, null=True, blank=True
    )
    platforms = models.ManyToManyField(ProjectPlatform, related_name='projects',blank=True)
    industries = models.ManyToManyField(ProjectIndustry, related_name='projects',blank=True)
    services = models.ManyToManyField(ProjectService, related_name='projects',blank=True)
    live_link = models.URLField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=True)
    in_active_at = models.DateField(null=True, blank=True)
    hourly_rate = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    activate_from = models.DateField(null=True,blank=True)
    featured_image = models.ImageField(null=True, blank=True)
    featured_video = models.URLField(null=True, blank=True)
    show_in_website = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag,related_name='projects')
    identifier = models.CharField(
        max_length=50,
        default=uuid4,  
    )
    is_highlighted = models.BooleanField(verbose_name="Is Highlighted?", default=False)
    is_team = models.BooleanField(verbose_name="Is Team?", default=False)
  
    project_results = models.OneToOneField(
        ProjectResults,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='project',
    )


        
    class Meta:
        ordering = ['title']
        permissions = [
             (
                "can_see_all_project_field",
                "Can See All Project Field",
            ),
    
        ]
           
        

    def clean(self):
        super().clean()

        if self.hourly_rate is not None and self.activate_from is None:
            raise ValidationError("If hourly rate is provided, activate from is mandatory.")
        if self.activate_from is not None and self.hourly_rate is None:
            raise ValidationError("If activate from is provided, hourly rate is mandatory.")
    
    def __str__(self):
            client_name = self.client.name if self.client else "No Client"
            return f"{self.title} ({client_name})"

    def durations(self):
        duration = datetime.datetime.now() - self.created_at
        return duration.days



    @property
    def created_at_timestamp(self):
        return int(self.created_at.strftime("%s")) * 1000

    def set_project_hours(self, value):
        self.total_project_hours = value

    def last_x_weeks_feedback(self, x):
        today = datetime.datetime.today()
        last_xth_friday = datetime.datetime.today() + relativedelta(weekday=FR(-x))

        return (
            self.clientfeedback_set.filter(
                created_at__date__lte=today,
                created_at__date__gt=last_xth_friday,
            )
            .order_by("-created_at")
            .exclude(project__active=False)
        )
    
    @property
    def check_is_weekly_project_hour_generated(self):
        latest_project_hour = ProjectHour.objects.filter(project=self).order_by("created_at").last()
        if latest_project_hour:
            latest_project_hour_date = latest_project_hour.created_at.date()
            # print(f"latest_project_hour_date: {latest_project_hour_date}")
            today = timezone.now().date()
            # print(f"today: {today}")
            last_friday = today - timedelta(days=(today.weekday() + 3) % 7)
            # print(f"last_friday: {last_friday}")
            if latest_project_hour_date < last_friday and today.weekday() in [4,5,6,0]:
                return False #RED
            else:
                return True #BLACK
        else:
            return True #BLACK
    
    @property
    def associated_employees(self):
        return Employee.objects.filter(
            employeeproject__project=self,
            employeeproject__project__active=True
        )



class ProjectDocument(TimeStampMixin, AuthorMixin):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=220)
    extra_note = models.TextField(null=True, blank=True)
    document = models.FileField(
        upload_to="uploads/project_documents/%y/%m",
    )


class ProjectToken(TimeStampMixin, AuthorMixin):
    project = models.OneToOneField(
        Project, limit_choices_to={"active": True}, on_delete=models.CASCADE
    )
    token = models.CharField(default=uuid4, max_length=255)

    def __str__(self) -> str:
        return f"{self.project.title} - {self.token[:-8]}"


class ProjectTechnology(TimeStampMixin, AuthorMixin):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    technologies = models.ManyToManyField(Technology)

    def __str__(self):
        return self.title
    
class OurTechnology(TimeStampMixin, AuthorMixin):
    title = models.CharField(max_length=200)
    technologies = models.ManyToManyField(Technology)


class ProjectScreenshot(TimeStampMixin, AuthorMixin):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField()


class ProjectContent(TimeStampMixin, AuthorMixin):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = HTMLField()
    image = models.ImageField(upload_to='project_images/', null=True, blank=True)
    image2 = models.ImageField(upload_to='project_images/', null=True, blank=True)

    def __str__(self):
        return self.title

class ProjectKeyFeature(TimeStampMixin, AuthorMixin):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = HTMLField()
    img = models.ImageField()
    img2 = models.ImageField(upload_to='project_images/', null=True, blank=True)
    def __str__(self):
        return self.title


class ProjectHour(TimeStampMixin, AuthorMixin):
    FORCAST_SELECTOR = (
        ("increase", "✔ Increase"),
        ("decrease", "⌛ Decrease"),
        ("same", "⌛ Same"),
        ("confused", "😕 Confused"),
    )
    HOUR_TYPE_SELECTOR = (
        ("project", "Project Hour"),
        ("bonus", "Bonus Project Hour"),
    )

    manager = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        limit_choices_to=(Q(active=True) & (Q(manager=True) | Q(lead=True))),
    )

    hour_type = models.CharField(
        max_length=40,
        choices=HOUR_TYPE_SELECTOR,
        default="project",
        verbose_name="Project Hour Type",
    )
    project = models.ForeignKey(
        Project,
        limit_choices_to={"active": True},
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    date = models.DateField()
    hours = models.FloatField()
    description = models.TextField(blank=True, verbose_name="Explanation")
    forcast = models.CharField(
        max_length=40,
        choices=FORCAST_SELECTOR,
        verbose_name="Forecast next week hours",
        null=True,
        blank=True,
    )
    payable = models.BooleanField(default=True)
    approved_by_cto = models.BooleanField(default=False)
    operation_feedback = models.URLField(blank=True, null=True, verbose_name="Operation Feedback")
    client_exp_feedback = models.URLField(blank=True, null=True, verbose_name="Client Experience Feedback")

    def __str__(self):
        return f"{self.project} | {self.manager}"

    def clean(self):
        
        if (
                self.date is not None
                and self.date.weekday() != 4
                and self.hour_type != "bonus"
        ):
            raise ValidationError({"date": "Today is not Friday"})
        if not self.project:
            raise ValidationError({"project":"You have to must assign any project"})
        
    def save(self, *args, **kwargs):
        # if not self.manager.manager:
        #     self.payable = False
        super(ProjectHour, self).save(*args, **kwargs)

    def employee_hour(self, employee_id):
        total = self.employeeprojecthour_set.aggregate(Sum("hours"))
        return employee_id, total["hours__sum"]

    class Meta:
        verbose_name_plural = "Weekly Project Hours"
        permissions = [
            ("show_all_hours", "Can show all hours just like admin"),
            ("select_hour_type", "Can select Project Hour type"),
            ("weekly_project_hours_approve", "Can approved and give feedback from CTO"),
        ]


class EmployeeProjectHour(TimeStampMixin, AuthorMixin):
    project_hour = models.ForeignKey(ProjectHour, on_delete=models.CASCADE)
    hours = models.FloatField()
    employee = models.ForeignKey(
        Employee,
        on_delete=models.RESTRICT,
        limit_choices_to={"active": True},
    )
    class Meta:
        permissions = [
            ("change_recent_activity", "Can change if inserted recently (3days)"),
            ("see_all_employee_hour", "Can see all emploployee project hour"),
        ]
        verbose_name = "Employee Project Hour"
        verbose_name_plural = "Employee Project Hours"
        verbose_name = "Employee Project Hour"
        verbose_name_plural = "Employee Project Hours"


class EmployeeProjectHourGroupByEmployee(EmployeeProjectHour):
    class Meta:
        proxy = True

        verbose_name = "Weekly Employee Hours"
        verbose_name_plural = "Weekly Employee Hours"

    def __str__(self) -> str:
        return self.project_hour.project.title


class DailyProjectUpdate(TimeStampMixin, AuthorMixin):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.RESTRICT,
        limit_choices_to={"active": True},
        related_name="dailyprojectupdate_employee",
    )
    manager = models.ForeignKey(
        Employee,
        on_delete=models.RESTRICT,
        limit_choices_to=(Q(active=True) & (Q(manager=True) | Q(lead=True))),
        related_name="dailyprojectupdate_manager",
        help_text="Manager / Lead",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.RESTRICT,
        related_name="projects",
        limit_choices_to={"active": True},
    )
    hours = models.FloatField(default=0.0)
    # description = models.TextField(blank=True, verbose_name='Explanation')
    update = models.TextField(null=True, blank=True, default=' ')
    updates_json = models.JSONField(null=True, blank=True)

    STATUS_CHOICE = (
        ("pending", "⌛ Pending"),
        ("approved", "✔ Approved"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default="pending")
    note = models.TextField(null=True, blank=True, help_text="Manager's note / remarks")

    # def clean(self):
    #     if self.hours < 4 and self.description == "":
    #         raise ValidationError({
    #             'description': f"Please explain why the hours is less than 4"
    #         })
    #     return super().clean()

    class Meta:
        permissions = [
            ("see_all_employee_update", "Can see all daily update"),
            ("can_approve_or_edit_daily_update_at_any_time", "Can approve or update daily project update at any time" ),
        ]
        verbose_name = "Daily Project Update"
        verbose_name_plural = "Daily Project Updates"


    @property
    def get_hours_history(self):
        historyData = ""
        if self.history is not None:
            for history in self.history.order_by("-created_at"):
                print(history)
                historyData += f"{history.hours}"
                if history != self.history.order_by("-created_at").last():
                    historyData += f" > "
            return format_html(historyData)

        return "No changes"

    @property
    def str_updates_json(self):
        # ic(self.updates_json)
        # out = '\n'.join([f"{i[0]} [{i[1]}]" for i in self.updates_json])
        # ic(out)
        if self.updates_json is not None:
            return '\n'.join([f"{i[0]} - {i[1]}H" for index, i in enumerate(self.updates_json)])
        # return '\n'.join(
        #     [f"{i[0]} - {i[1]}H {i[2] if (lambda lst, idx: True if idx < len(lst) else False)(i, 2) else ''} " for
        #      index, i in enumerate(self.updates_json)])
        else:
            return str(self.update)

    # def clean(self):
    #     # LeaveManagement = apps.get_model('employee', 'LeaveManagement')
    #     # if len(LeaveManagement.objects.filter(manager=self.manager, status='pending')) > 0:
    #     if len(self.employee.leave_management_manager.filter(status='pending')) > 0:
    #         raise ValidationError('You have pending leave application(s). Please approve first.')


class DailyProjectUpdateHistory(TimeStampMixin, AuthorMixin):
    daily_update = models.ForeignKey(
        DailyProjectUpdate, on_delete=models.CASCADE, related_name="history"
    )
    hours = models.FloatField(default=0.0)


class DailyProjectUpdateAttachment(TimeStampMixin, AuthorMixin):
    daily_update = models.ForeignKey(
        DailyProjectUpdate,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Daily Project Update",
    )
    title = models.CharField(max_length=220)
    attachment = models.FileField(
        verbose_name="Document",
        upload_to="uploads/daily_update/%y/%m",
        null=True,
        blank=True,
    )


class DailyProjectUpdateGroupByEmployee(DailyProjectUpdate):
    class Meta:
        proxy = True

        permissions = [
            ("see_all_employee_update", "Can see all daily update"),
        ]
        verbose_name = "Group By Employee"
        verbose_name_plural = "Group By Employee"

    def __str__(self) -> str:
        return self.project.title


class DailyProjectUpdateGroupByProject(DailyProjectUpdate):
    class Meta:
        proxy = True
        permissions = [
            ("see_all_employee_update", "Can see all daily update"),
        ]
        verbose_name = "Group By Project"
        verbose_name_plural = "Group By Project"

    def __str__(self) -> str:
        return self.project.title


class DailyProjectUpdateGroupByManager(DailyProjectUpdate):
    class Meta:
        proxy = True
        permissions = [
            ("see_all_employee_update", "Can see all daily update"),
        ]
        verbose_name = "Group By Manager"
        verbose_name_plural = "Group By Manager"

    def __str__(self) -> str:
        return self.project.title


class DurationUnit(TimeStampMixin, AuthorMixin):
    title = models.CharField(max_length=200)
    duration_in_hour = models.FloatField(default=1)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ProjectResource(TimeStampMixin, AuthorMixin):
    project = models.ForeignKey(
        Project, limit_choices_to={"active": True}, on_delete=models.CASCADE
    )
    manager = models.ForeignKey(
        Employee,
        limit_choices_to={"manager": True, "active": True},
        on_delete=models.CASCADE,
    )
    active = models.BooleanField(default=True)


class ProjectResourceEmployee(TimeStampMixin, AuthorMixin):
    project_resource = models.ForeignKey(
        ProjectResource, limit_choices_to={"active": True}, on_delete=models.CASCADE
    )
    employee = models.ForeignKey(
        Employee,
        limit_choices_to={
            "active": True,
            "manager": False,
            "employeeskill__isnull": False,
        },
        on_delete=models.CASCADE,
    )
    duration = models.FloatField(
        max_length=200, help_text="Estimated Project End Duration"
    )
    duration_unit = models.ForeignKey(
        DurationUnit, limit_choices_to={"active": True}, on_delete=models.CASCADE
    )
    duration_hour = models.FloatField()
    hour = models.FloatField(
        max_length=200,
        help_text="Estimated hours for each week",
        null=True,
        default=True,
    )

    def clean(self):
        if (
                ProjectResourceEmployee.objects.filter(employee=self.employee)
                        .exclude(id=self.id)
                        .first()
        ):
            raise ValidationError(
                {
                    "employee": f"{self.employee} is already been taken in another project"
                }
            )

    def save(self, *args, **kwargs):
        self.duration_hour = self.duration * self.duration_unit.duration_in_hour
        super().save(*args, **kwargs)

    @property
    def end_date(self):
        return self.updated_at + timedelta(hours=self.duration_hour)

    @property
    def endways(self):
        return self.end_date <= today() + timedelta(days=7)


class ProjectNeed(TimeStampMixin, AuthorMixin):
    technology = models.CharField(max_length=255)
    quantity = models.IntegerField()
    note = models.TextField(null=True, blank=True)


class ClientFeedback(AuthorMixin, TimeStampMixin):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    feedback_week = models.DateField(null=True)

    feedback = models.TextField()
    avg_rating = models.FloatField()

    rating_communication = models.FloatField()
    rating_output = models.FloatField()
    rating_time_management = models.FloatField()
    rating_billing = models.FloatField()
    rating_long_term_interest = models.FloatField()

    @property
    def has_red_rating(self):
        red_line = 3.5

        return (
                self.rating_communication <= red_line
                or self.rating_output <= red_line
                or self.rating_time_management <= red_line
                or self.rating_billing <= red_line
                or self.rating_long_term_interest <= red_line
        )

    class Meta:
        permissions = (
            ("can_see_client_feedback_admin", "Can see Client Feedback admin"),
        )

    def save(self, *args, **kwargs):
        avg_rating = (
                self.rating_communication
                + self.rating_output
                + self.rating_time_management
                + self.rating_billing
                + self.rating_long_term_interest
        )
        avg_rating = round(avg_rating / 5, 1)
        self.avg_rating = avg_rating
        super(ClientFeedback, self).save(*args, **kwargs)
        self.feedback_week = self.created_at + relativedelta(weekday=FR(-1))
        return super(ClientFeedback, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.project.title} ({str(self.avg_rating)})"


class CodeReview(TimeStampMixin, AuthorMixin):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, limit_choices_to={"active": True}
    )
    manager = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        limit_choices_to={"active": True, "manager": True},
        null=True,
        related_name="mange",
        blank=True,
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, limit_choices_to={"active": True}
    )

    naming_convention = models.FloatField()
    code_reusability = models.FloatField()
    oop_principal = models.FloatField()
    design_pattern = models.FloatField()
    standard_git_commit = models.FloatField()
    review_at = models.DateTimeField(auto_now_add=False, null=True)

    avg_rating = models.FloatField()

    comment = models.TextField()

    for_first_quarter = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        avg_rating = (
                self.naming_convention
                + self.code_reusability
                + self.oop_principal
                + self.design_pattern
                + self.standard_git_commit
        )
        avg_rating = round(avg_rating / 5, 1)
        self.avg_rating = avg_rating

        super(CodeReview, self).save(*args, **kwargs)

        if not self.created_at.date().day <= 15:
            self.for_first_quarter = False

        super(CodeReview, self).save(*args, **kwargs)

    class Meta:
        permissions = (("can_give_code_review", "Can give code review"),)


class CodeReviewEmployeeFeedback(TimeStampMixin, AuthorMixin):
    code_review = models.ForeignKey(CodeReview, on_delete=models.CASCADE)
    comment = models.TextField()


class ProjectReport(TimeStampMixin):
    TYPE_CHOICE = (
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("lead", "Lead"),
        ("sqa", "SQA")
    )
    name = models.CharField(max_length=255, null=True)
    project = models.ForeignKey(
        Project, related_name='project_reports',
        limit_choices_to={"active": True},
        on_delete=models.CASCADE
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICE, default="manager")
    send_to = models.CharField(
        verbose_name="Send To", max_length=255
    )
    api_token = models.TextField(verbose_name='API Token')

    class Meta:
        verbose_name = "Project Report"
        verbose_name_plural = "Project Reports"

    def __str__(self):
        return f"{self.project} update to {self.send_to}"

    class Meta:
        verbose_name = "Project Report"
        verbose_name_plural = "Project Reports"


class EnableDailyUpdateNow(AuthorMixin, TimeStampMixin):
    name = models.CharField(max_length=24)
    enableproject = models.BooleanField(default=False)
    last_time = models.TimeField(null=True, blank=True)

    def clean(self):
        if self.last_time is None:
            raise ValidationError("Please Enter Last Time")
        # Ensure only one object of this class exists
        # if not self.pk and EnableDailyUpdateNow.objects.exists():
        #     raise ValidationError("Only one instance of EnableDailyUpdateNow can be created. And One instance is already exist.")


    def save(self, *args, **kwargs):
        # Ensure only one object of this class exists
        # if not self.pk and EnableDailyUpdateNow.objects.exists():
        #     # If trying to create a new object and one already exists, raise an exception
        #     raise Exception("Only one instance of EnableDailyUpdateNow can be created.")
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if EnableDailyUpdateNow.objects.count() <= 1:
            raise ValidationError("At least one instance of EnableDailyUpdateNow must remain in the database.")
        return super().delete(*args, **kwargs)
    class Meta:
        verbose_name = "Project Update Enable"
        verbose_name_plural = "Project Update Enable by me"
        # permissions = (("can_change_daily_update_any_time", "Can change daily Update any Time"),)


class ObservationProject(TimeStampMixin, AuthorMixin):
    project_name = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, related_name='observation_projects')
    class Meta:
        verbose_name = 'Observe New Project'
        # verbose_name_plural = 'Observations'
@receiver(post_save, sender=Project)
def create_observation(sender, instance, created, **kwargs):
    if created:
        ObservationProject.objects.create(project_name=instance)

@receiver(post_save, sender=ProjectHour)
def create_income(sender, instance, created, **kwargs):
    print('sssssssssssssssssssssss create income has called ssssssssssssssssssss')
    from account.models import Income

    if created:
        project = instance.project
        if project:
            Income.objects.create(
                project=project,
                hours=instance.hours,
                hour_rate=project.hourly_rate if project.hourly_rate is not None else 0.00,
                convert_rate=90.0,  # Default convert rate
                date=instance.date,
                status="pending"
            )