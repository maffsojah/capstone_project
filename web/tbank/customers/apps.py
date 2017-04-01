# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class EmployeesConfig(ModuleMixin, AppConfig):
    name = 'customers'
    icon = '<i class="material-icons">people</i>'
