from debug_toolbar.middleware import DebugToolbarMiddleware
from django.utils.deprecation import MiddlewareMixin


class AtopdedTo110DebugMiddleware(MiddlewareMixin, DebugToolbarMiddleware):
    pass
