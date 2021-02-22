from functools import wraps
from flask_login import current_user
from flask import abort
from jobplus.models import User


def role_required(role):
    """带参数的装饰器,可以使用它保护一个路由函数被特定角色访问"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role < role:
                abort(404)
            return func(*args, **kwargs)
        return wrapper
    return decorator


# 特定用户的装饰器
admin_required = role_required(User.ROLE_ADMIN)


