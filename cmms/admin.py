from django.contrib import admin
from cmms.models import SysUser,WorkOrder

# Register your models here.
admin.site.register(SysUser)
admin.site.register(WorkOrder)
admin.site.site_header = 'پنل مدیریت اکسپرتر سرورایان'
admin.site.site_title = 'پنل مدیریت اکسپرتر سرورایان'
admin.site.index_title = 'به پنل مدیریت اکسپرتر سرو رایان  خوش آمدید'