from django.db import models
from django.utils.translation import ugettext_lazy as _


class QuoteStatus(models.TextChoices):
    """
    Status of QuoteItem
    """
    waiting = 'waiting', _('waiting')
    submitting = 'submitting', _('submitting')
