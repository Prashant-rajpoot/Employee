from django.template.loader import get_template
import datetime
from django.core.mail import EmailMultiAlternatives

from holidays.selectors import get_all_holidays


def send_leave_application_email(approvers, leave_application, domain=None):
    approver_emails = []
    for approver in approvers:
        approver_emails.append(approver.email)

    context = {
        'applicant_name': leave_application.employee,
        'server_url': domain
    }

    subject, from_mail, to = 'New Leave Application', None, approver_emails
    html_content = get_template('email/application_notification.html').render(context)
    msg = EmailMultiAlternatives(subject, None, from_mail, to)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_leave_plan_email(approvers, leave_plan, domain=None):
    approver_emails = []
    for approver in approvers:
        approver_emails.append(approver.email)

    context = {
        'applicant_name': leave_plan.employee,
        'server_url': domain
    }

    subject, from_mail, to = 'New Leave Plan', None, approver_emails
    html_content = get_template('email/application_notification.html').render(context)
    msg = EmailMultiAlternatives(subject, None, from_mail, to)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_leave_response_email(leave_application, approver, status, domain=None):
    applicant = leave_application.employee
    user = applicant.solitonuser.user

    context = {
        'applicant': applicant,
        'leave_application': leave_application,
        'approver': approver,
        'status': status,
        'server_url': domain
    }

    subject, from_mail, to = 'Leave Application Response', None, user.email
    html_content = get_template('email/response_notification.html').render(context)
    msg = EmailMultiAlternatives(subject, None, from_mail, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def get_number_of_days_without_public_holidays(start_date, end_date):
    from_date = start_date
    to_date = end_date
    date_difference = to_date - from_date
    all_days_between = (date_difference.days + 1)
    # Getting all holiday objects
    holidays = get_all_holidays()
    public_days = 0
    k = 0
    while k <= all_days_between:
        time = datetime.datetime.min.time()
        front_date_datetime = datetime.datetime.combine(from_date, time)
        check_date = front_date_datetime + datetime.timedelta(days=k)
        is_holiday = holidays.filter(date=check_date.date()).exists()

        if check_date.weekday() == 6 or is_holiday:
            public_days += 1

        k = k + 1

    no_of_days = all_days_between - public_days
    return no_of_days


def expire_leave_plan_application(application, no_of_days: int) -> bool:
    if not application.expired:
        today = datetime.date.today()
        # Application expiry date
        expiry_date = application.plan_date + datetime.timedelta(days=no_of_days)
        if today == expiry_date or today > expiry_date:
            application.expired = True
            application.approval_status = "Expired"
            application.save()
            return True
        else:
            return False
    else:
        return False


def expire_leave_application(application) -> bool:
    if not application.expired:
        today = datetime.date.today()
        # Application expiry date
        expiry_date = application.start_date
        if today == expiry_date or today > expiry_date:
            application.expired = True
            application.overall_status = "Expired"
            application.save()
            return True
        else:
            return False
    else:
        return False
