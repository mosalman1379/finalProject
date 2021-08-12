import datetime

from django.dispatch import receiver, Signal

from sale.models import EmailHistory, Quote

email_signal=Signal()


@receiver(email_signal)
def create_model(sender,**kwargs):
    if 'Quote' in str(sender):
        instance = kwargs['instance']
        if kwargs['success']:
            EmailHistory.objects.create(email=instance.organization.email,success=True
                                        ,date=datetime.datetime.now(),user_id=instance.organization.registrant_user.pk)
        else:
            EmailHistory.objects.create(email=instance.organization.email, success=False
                                        , date=datetime.datetime.now(),user_id=instance.organization.registrant_user.pk)

