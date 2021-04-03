from cmms.models import Stock
from cmms.business.WOUtility import *
from cmms.business.systemmessage import *
from django.core.paginator import *
class StockUtility:
    @staticmethod
    def remove(wopart):
        if(wopart.woPartWorkorder.isScheduling==False):
            stock=Stock.objects.get(id=wopart.woPartStock.id)
            if(stock.qtyOnHand>=wopart.woPartActulaQnty):
                stock.qtyOnHand-=wopart.woPartActulaQnty
                stock.save()
                return WOPartMsg.Success
            else:
                wopart.woPartActulaQnty=0
                # WOUtility.changeWoStatus2Waiting4Part(wopart.woPartWorkorder)
                woObj=WorkOrder.objects.get(id=wopart.woPartWorkorder.id)
                woObj.woStatus=9
                # print("#$%^#@$@#$@#$@#$@#"+str(wopart.woPartWorkorder.woStatus))
                woObj.save()

            # Send message to admin that wopart is not enough

                return WOPartMsg.NotEnouphPart
        else:
            return WOPartMsg.Pass
    # @staticmethod
    # def removeAssetPart(assetpart):
    #
    #         stock=Stock.objects.get(id=assetpart.assetPartPid.id)
    #         if(stock.qtyOnHand>=wopart.woPartActulaQnty):
    #             stock.qtyOnHand-=wopart.woPartActulaQnty
    #             stock.save()
    #             return WOPartMsg.Success
    #         else:
    #             wopart.woPartActulaQnty=0
    #             # WOUtility.changeWoStatus2Waiting4Part(wopart.woPartWorkorder)
    #             woObj=WorkOrder.objects.get(id=wopart.woPartWorkorder.id)
    #             woObj.woStatus=9
    #             # print("#$%^#@$@#$@#$@#$@#"+str(wopart.woPartWorkorder.woStatus))
    #             woObj.save()
    #
    #         # Send message to admin that wopart is not enough
    #
    #             return WOPartMsg.NotEnouphPart
    #     else:
    #         return WOPartMsg.Pass
    @staticmethod
    def add(stc,amount):
        stock=Stock.objects.get(id=stc.id)
        stock.qtyOnHand+=amount
        stock.save()
        return WOPartMsg.Success
    @staticmethod
    def have_Prev_val(stockInstance):
        val=Stock.objects.filter(stockItem=stockInstance.stockItem,location=stockInstance.location)
        if(val):
            return True
        else:
            return False
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
    #نمایش اطلاعات مصرف برای یک انبار
    @staticmethod
    def getConsumeInfo(stockID,num):
        return WorkorderPart.objects.raw("select * from workorderpart where woPartStock_id={0} order by id limit {1},5 ".format(stockID,num))
    #نمایش اطلاعات مصرف برای یک انبار
    @staticmethod
    def getPurchasedInfo(stockID,num):
        return PartPurchase.objects.raw("select * from partpurchase where purchaseStock_id={0} order by id limit {1},5 ".format(stockID,num))
    @staticmethod
    def seachStock(searchStr):

        if(not searchStr):


            return Stock.objects.all().order_by('-id')
        return Stock.objects.filter(stockItem__partName__contains=searchStr).order_by('-id')
    @staticmethod
    def haveEnoughStock(wopart ):#tedad:tedad ghate ke mikhahad masraf shavad
        if(wopart.woPartWorkorder.isScheduling==False):
            stock=wopart.woPartStock
            if(stock.qtyOnHand>=wopart.woPartActulaQnty):

                return WOPartMsg.Success
            else:
                wopart.woPartActulaQnty=0
                # WOUtility.changeWoStatus2Waiting4Part(wopart.woPartWorkorder)
                woObj=WorkOrder.objects.get(id=wopart.woPartWorkorder.id)
                woObj.woStatus=9
                # print("#$%^#@$@#$@#$@#$@#"+str(wopart.woPartWorkorder.woStatus))
                woObj.save()

            # Send message to admin that wopart is not enough

                return WOPartMsg.NotEnouphPart
        else:
            return WOPartMsg.Pass
    @staticmethod
    def getStockParts(searchStr):
        return Stock.objects.filter(stockItem__partName__isnull=False,stockItem__partName__contains=searchStr).values('id', 'stockItem__partName')
