from __future__ import unicode_literals

from material.frontend.apps import ModuleMixin
from django.apps import AppConfig


class ServicesConfig(ModuleMixin, AppConfig):
    name = 'services'
    icon = '<i class="material-icons">suare-inc-cash</i>'
