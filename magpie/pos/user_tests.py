"""
UserPassesTestMixin Tests
"""
def active_aa_su(_user):
    """
    Test if user is:
    Is Active
    and
    Is Accounts Admin
    or
    Is Superuser
    """
    test_result = False
    if _user.is_active and _user.is_accounts_admin:
        test_result = True
    if _user.is_superuser:
        test_result = True
    return test_result

def active_md_dm_su(_user):
    """
    Test if user is:
    Is Active and Is Manager
    or
    Is Active and Is Director
    or
    Is Active and Is Superuser
    """
    test_result = False
    if _user.is_active and _user.is_manager:
        test_result = True
    if _user.is_active and _user.is_director:
        test_result = True
    if _user.is_active and _user.is_active:
        test_result = True
    return test_result

def active_staff_su(_user):
    """
    Test is user is:
    Is Active and Is Staff
    or
    Is Active and Is Superuser
    """
    test_result = False
    if _user.is_active and _user.is_staff:
        test_result = True
    if _user.is_active and _user.is_superuser:
        test_result = True
    return test_result
