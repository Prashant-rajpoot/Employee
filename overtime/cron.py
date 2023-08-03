from overtime.selectors import get_all_non_expired_overtime_applications
from overtime.services import expire_overtime_application


def expire_overtime_applications():
    non_expired_overtime_applications = get_all_non_expired_overtime_applications()
    for overtime_application in non_expired_overtime_applications:
        expire_overtime_application(overtime_application, 10)  # Expires every 10 days
    return True
