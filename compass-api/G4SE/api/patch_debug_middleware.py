from debug_toolbar.middleware import DebugToolbarMiddleware
from django.utils.deprecation import MiddlewareMixin


class AdopdedTo110DebugMiddleware(MiddlewareMixin, DebugToolbarMiddleware):
    pass
