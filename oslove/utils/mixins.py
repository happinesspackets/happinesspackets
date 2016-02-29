from __future__ import unicode_literals
from axes.decorators import watch_login
from django.utils.decorators import method_decorator


class AxesControlledMixin(object):
    """
    Wrap this view in django-axes' watch-login. Must only be applied to form views.
    Every form submission failure counts towards the AXES_LOGIN_FAILURE_LIMIT,
    so do not apply this to all forms - only those sensitive to bruteforcing.
    """
    @method_decorator(watch_login)
    def dispatch(self, request, *args, **kwargs):
        return super(AxesControlledMixin, self).dispatch(request, *args, **kwargs)
