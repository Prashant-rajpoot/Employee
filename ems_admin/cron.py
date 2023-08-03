from ems_admin.selectors import get_all_audit_trails


def delete_all_audit_trails():
    audit_trails = get_all_audit_trails()
    for audit_trail in audit_trails:
        audit_trail.delete()
