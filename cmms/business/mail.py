from cmms.models.users import *
from cmms.models.message import *
class Mail:
    @staticmethod
    def SendNewSysMessage(r,title,priority=None,msgid=None,wo=None):
        print(r)
        print(title)

        if(priority==None):
            priority=5 #lowest val
        sysuser=SysUser.objects.get(id=1)
        touser=SysUser.objects.get(userId__username=r)
        msg="""<p>یک سفارش کاری جدید برای {} ایجاد گردید</p>


        <p>خلاصه درخواست:<br/>{}</p>".format(touser.fullName,title)
        <a class='btn btn-warning btn-rounded' href='/WorkOrder/{0}/details'>
											مشاهده دستور کار</a>

        """.format(msgid)
        sub="سفارش کاری    جدید ایجاد شد"
        Message.objects.create(subject=sub,messageStatus=2,fromUser=sysuser,toUser=touser,Message=msg,msgPririty=priority,workOrder=wo)

    def SendUpdatedSysMessage(r,title,priority=None,msgid=None,wo=None):

       if(priority==None):
            priority=5 #lowest val
       mails=Message.objects.filter(workOrder=wo)
       for i in mails:
           i.delete()
       print(msgid,"############")
       sysuser=SysUser.objects.get(userId__username="admin")
       touser=SysUser.objects.get(userId__username=r)
       sub="سفارش کاری بروز گردانی شد"
       msg="""<p>سفارش کاری برای کاربر {0} بروز گردید.</p>
       <a class='btn btn-warning btn-rounded' href='/WorkOrder/{1}/details'>
                                           مشاهده دستور کار</a>

       <p>خلاصه درخواست:<br/>{2}</p>""".format(touser.fullName,msgid,title)
       Message.objects.create(subject=sub,messageStatus=2,fromUser=sysuser,toUser=touser,Message=msg,msgPririty=priority)
