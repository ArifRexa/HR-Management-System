from django.core.mail import EmailMultiAlternatives
from threading import Thread
from django.template import loader



class EmailTread(Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(
            self.subject, 
            self.html_content, 
            '"Mediusware-Career" <career@mediusware.com>',
            self.recipient_list
        )
        msg.attach_alternative(self.html_content, "text/html")
        msg.send()

def send_mail(subject, html_content, recipient_list):
    EmailTread(subject, html_content, recipient_list).start()


#===============================================================================================

def re_apply_alert_mail(candidate):
    if candidate is not None:
        subject = f"Request to Re-apply through the Job Portal"
        html_content = loader.render_to_string('mail/re_apply_alert.html', {'candidate': candidate})
        send_mail(subject, html_content, [candidate.email])












    #     designation = employee.designation
    # full_name = employee.full_name
    # if employee is not None and extra_data is not None:
    #     watting_from = extra_data['waitting_at']
    #     subject = f"{employee.full_name}, needs CTO Help!!!"
    #     html_content = loader.render_to_string('mails/cto_help.html', {'title': subject, 'designation': designation, 'full_name': full_name, 'watting_from': watting_from})
    #     send_mail(subject, html_content, extra_data['receiver'])
