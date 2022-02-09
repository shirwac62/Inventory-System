import uuid

from flask_login import current_user


def generate_uuid():
    return str(uuid.uuid4())


def get_current_user():
    if current_user and current_user.is_authenticated:
        return current_user.id
    else:
        return None



def get_user_branch():
    if current_user and current_user.is_authenticated:
        if current_user.branch_id:
            return current_user.branch_id
    return None


def get_user_branches():
    if current_user and current_user.is_authenticated:
        return [a.id for a in current_user.branches]
    return []
