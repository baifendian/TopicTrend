# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('eventsflow.views',
    url(r"^events/$", "events"),
    url(r"^events/lifetime/$", "lifetime"),
)


