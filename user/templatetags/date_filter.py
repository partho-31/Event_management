from django import template
from datetime import datetime
from django.utils import timezone

register = template.Library()

@register.filter
def CustomDate(value):
    if value:
        DateNow = datetime.now().date()
        val = timezone.localtime(value)
        if DateNow == val.date():
            return f"Today at {val.strftime('%I : %M %p')}"
        elif DateNow.replace(day= DateNow.day - 1) == val.date():
            return f"Yesterday at {val.strftime('%I : %M %p')}"
        else:
            return f"{val.date().strftime('%B %d')},{val.strftime('%I : %M %p')}"
    return f"No login record exsits"
