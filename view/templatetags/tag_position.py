from django.template import Library
from  django.utils.timesince import timesince

from api.models import WarningEvent

register = Library()


# return time of notifications - current time
@register.simple_tag()
def get_warnings(position):
    return len(WarningEvent.objects.filter(position=position))
