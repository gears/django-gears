from django.conf import settings
from django.conf.urls import patterns, url

from .settings import GEARS_URL
from .views import serve


def gears_urlpatterns(prefix=None):
    prefix = prefix or GEARS_URL.strip("/")

    if settings.DEBUG:
        return patterns("",
            url(
                regex=r"^{0}/(?P<path>.*)$".format(prefix),
                view=serve,
            ),
        )
    else:
        return patterns("")
