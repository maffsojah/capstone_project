# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class ServicesConfig(ModuleMixin, AppConfig):
    name = 'services'
    icon = '<i class="material-icons">settings_applications</i>'
    verbose_name = "Bank Services"

    def has_perm(self, user):
        return user.is_authenticated()
