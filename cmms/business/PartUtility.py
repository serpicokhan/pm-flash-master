from cmms.models import *
import jdatetime
import datetime
from django.core.paginator import *
from django.db.models import Count
class PartUtility:
    @staticmethod
    def getUsedPartNum(start,end):
        # print("SELECT  count(woPartActulaQnty) as id   from workorderpart inner join workorder on  workorderpart.woPartWorkorder_id=workorder.id where workorder.datecreated  between '{0}' and '{1}' and isScheduling=0".format(start,end))
        return WorkorderPart.objects.raw("SELECT  count(woPartActulaQnty) as id   from workorderpart inner join workorder on  workorderpart.woPartWorkorder_id=workorder.id where (workorder.datecreated)  between '{0}' and '{1}' and isScheduling=0".format(start,end))
    @staticmethod
    def getPartCost(start,end):
        return WorkorderPart.objects.raw("""SELECT  sum(t1.woPartActulaQnty*t2.partLastPrice) as id  from workorderpart
        as t1  inner join stocks s1 on s1.stockItem_id=t1.woPartStock_id

        inner join parts as t2 on s1.stockItem_id=t2.id
        inner join workorder as t3 on  t1.woPartWorkorder_id=t3.id where date(t1.timeStamp)  between '{0}' and '{1}'
        and isScheduling=0""".format(start,end))
    @staticmethod
    def getPartCostForAsset(assetId,start,end):
        # print("getPartCostForAsset",":13")
        # print("SELECT  sum(t1.woPartActulaQnty*t2.partLastPrice) as id  from workorderpart as t1 join parts as t2 on t1.woPartPart_id=t2.id  inner join workorder as t3 on  t1.woPartWorkorder_id=t3.id where t1.timeStamp  between '{0}' and '{1}' and isScheduling=0 and t3.woAsset_id={2}".format(start,end,assetId))
        return WorkorderPart.objects.raw("""SELECT  sum(t1.woPartActulaQnty*t2.partLastPrice) as id
        from workorderpart as t1 inner join stocks s1 on s1.id=t1.woPartStock_id
        inner join parts as t2 on s1.stockItem_id=t2.id
        inner join workorder as t3 on  t1.woPartWorkorder_id=t3.id
        where date(t1.timeStamp)  between '{0}' and '{1}' and t3.isScheduling=0 and t3.woAsset_id={2}""".format(start,end,assetId))
    @staticmethod
    def doPaging(request,books):
        page=request.GET.get('page',1)
        paginator = Paginator(books, 10)
        wos=None
        try:
            wos=paginator.page(page)
        except PageNotAnInteger:
            wos = paginator.page(1)
        except EmptyPage:
            wos = paginator.page(paginator.num_pages)
        return wos
    @staticmethod
    def getParts(searchStr):
        return Part.objects.filter(partName__isnull=False).filter(partName__contains=searchStr).values('id', 'partName')
    @staticmethod
    def getPartStock(partId):
        retStr="<select id='id_woPartStock'>"
        x=Stock.objects.filter(stockItem=partId)
        for i in x:
            retStr+="<option value={0}>{1}</option>".format(i.id,i.location)
        retStr+="</select>"
        return retStr
############# search Part in partlist.html
    @staticmethod
    def seachPart(searchStr):
         # print("43 partutility$$$$$$$$$$$$$$$$$$$")
         # print("select id from parts where (partname like '%{}%') or (partDescription like '%{}%') or (partcode like '%{}%') or (partModel like '%{}%') order by id desc".format(searchStr,searchStr,searchStr,searchStr))
         if(searchStr != 'empty'):
             return Part.objects.filter(partName__contains=searchStr)|Part.objects.filter(partCode__contains=searchStr) #raw("select id from parts where (partname like '\%@p\%') or (partDescription like 'p') or (partcode like 'p') or (partModel like 'p') order by id desc")
         # return WorkOrder.objects.filter(summaryofIssue__isnull=False,isScheduling=False,woTags__contains=searchStr).order_by('-id')
         else:
             return Part.objects.all()


    @staticmethod
    def getPartMaintenancePie(id):

        n1=WorkorderPart.objects.raw(""" select   sum(t1.woPartActulaQnty) as id,t3.name as mname from workorderpart t1
                                    inner join stocks s1 on s1.id=t1.woPartStock_id
                                     inner join workorder t2 on t1.woPartWorkorder_id=t2.id
                                     inner join maintenancetype t3 on t2.maintenanceType_id=t3.id
                                     where s1.stockItem_id={0} and t2.isscheduling=0 and pyear(t1.timeStamp)=pyear(current_date)

                                     group by (t3.id) """.format(id))
        return n1
    @staticmethod
    def getWoPartUsageHistory(id):
        n1=WorkorderPart.objects.raw(""" select sum(woPartActulaQnty) as id , pmonth(t1.timeStamp) as month
                                     from workorderpart as t1

                                     inner join workorder t2 on t1.woPartWorkorder_id=t2.id
                                     inner join stocks s1 on s1.id=t1.woPartStock_id
                                     where s1.stockitem_id={0}
                                     and t2.isscheduling=0 and pyear(t1.timeStamp)=pyear(current_date)
                                     group by(pmonth(t1.timeStamp) )

                                     """.format(id))
        return n1

    @staticmethod
    def getPartPurchaseHistory(id):
        n1=PartPurchase.objects.raw("""select sum(purchaseQuantityReceived) as id,pmonth(purchaseDateRecieved) as month
                                    from partpurchase
                                    where purchasePartId_id={0}  and pyear(purchaseDateRecieved)=pyear(current_date)
                                    group by(pmonth(purchaseDateRecieved))
                                    """.format(id))
        return n1




    @staticmethod
    def getConsumeInfo(id,num):
        return WorkorderPart.objects.filter(woPartStock__stockItem__id=id)[:5]#raw("select * from workorderpart where woPartPart_id={0} order by id limit {1},5 ".format(id,num))
    #نمایش اطلاعات مصرف برای یک انبار
    @staticmethod
    def getPurchasedInfo(id,num):
        return PartPurchase.objects.raw("select * from partpurchase where purchasePartId_id={0} order by id limit {1},5 ".format(id,num))
