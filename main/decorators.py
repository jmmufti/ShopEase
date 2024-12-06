from django.core.exceptions import PermissionDenied
from functools import wraps

def buyer_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.role == 'buyer':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def seller_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.role == 'seller':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap