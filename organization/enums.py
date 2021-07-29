from django.db import models
from django.utils.translation import ugettext_lazy as _


class OrganizationStatus(models.TextChoices):
    in_progress = 'in-progress', _('in progress')
    final_registration = 'final-registration', _('final registration')
