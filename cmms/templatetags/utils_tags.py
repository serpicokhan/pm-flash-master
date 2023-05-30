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
@register.filter
def show_hour(value):
    return '{0:02.0f}:{1:02.0f}'.format(*divmod(float(value) * 60, 60))
@register.filter
def get_value_by_date(data_list, date):
    for data in data_list:
        print(data['date'],date)
        if data['date'] == date:
            return data['value']
    return ''
