from django import template
import jdatetime


register = template.Library()

@register.filter
def get_jalali(value):

    return jdatetime.date.fromgregorian(date=value)
@register.filter
def get_filter_action(value):
    if(value==1):
        return "ایجاد"
    elif(value==2):
        return "ویرایش"
    elif(value==3):
        return "حذف"
    else:
        return "نامشخص"
