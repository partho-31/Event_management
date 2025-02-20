from django import template
from datetime import datetime
from django.utils import timezone

register = template.Library()

@register.filter
def CustomDate(value):
    if value:
        DateNow = datetime.now().date()
        value = timezone.localdate(value)
        if DateNow == value.date():
            return f"Today at {value.strftime('%I : %M %p')}"
        elif DateNow.replace(day= DateNow.day - 1) == value.date:
            return f"Yesterday at {value.strftime('%I : %M %p')}"
        else:
            return f"{value.strftime('%B %d')} {value.strftime('%I : %M %p')}"
    return f"No login record exsits"
