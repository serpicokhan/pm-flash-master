from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from cmms.models import *
from cmms.business.mail import Mail
import sys
from cmms.business.stockutility import *
from django.core.exceptions import ObjectDoesNotExist
from pprint import pprint


# def create_wo(unit):
#     ##### Create Wo #########
#     stableWo=WorkOrder.objects.get(id=unit.workOrder_id)
#     oldWo=WorkOrder.objects.get(id=unit.workOrder_id)
#     stableWo.pk=None
#     stableWo.visibile=True
#     stableWo.isScheduling=False
#     stableWo.isPm=True
#     stableWo.datecreated=datetime.now().date()
#     stableWo.timecreated=datetime.now().time()
#     stableWo.isPartOf=unit.workOrder
#     # Newsch.schNextWo=WorkOrder.objects.create(datecreated=Newsch.schnextTime.date(),timecreated=Newsch.schnextTime.time(),visibile=False,isScheduling=False,isPartOf=Newsch.workOrder)
#     stableWo.save()
#
#     #################
#     # wt=WorkorderTask.objects.filter(workorder=oldWo)
#     wt=Tasks.objects.filter(workorder=oldWo)
#     if(wt!=None):
#         for f in wt:
#             f.pk=None
#             f.workorder=stableWo
#             f.save()
#     ##############
#     wp=WorkorderPart.objects.filter(woPartWorkorder=oldWo)
#     if(wp!=None):
#         for f in wp:
#             f.pk=None
#             f.woPartWorkorder=stableWo
#             woPartMsg=StockUtility.remove(f)
#             f.save()
#     ###############
#     wf=WorkorderFile.objects.filter(woFileworkorder=oldWo)
#     if(wf!=None):
#
#         for f in wf:
#             f.pk=None
#             f.woFileworkorder=stableWo
#             f.save()
#
#     ################
#     try:
#         wn=get_object_or_404(WorkorderUserNotification,woNotifWorkorder=oldWo)
#         if(wn!=None):
#             wn.pk=None
#             wn.woNotifWorkorder=stableWo
#             wn.save()
#     except:
#         print("error")
#
@receiver(pre_save, sender=PartPurchase )
def save_purchasepart_profile(sender, instance, **kwargs):
    stock=Stock.objects.none()
    # pass
    if(instance.id):
        oldVal=PartPurchase.objects.get(id=instance.pk)
        try:
            stock=Stock.objects.get(stockItem=instance.purchasePartId,location=instance.purchaseStock)
            stock.qtyOnHand-=oldVal.purchaseQuantityReceived
            stock.qtyOnHand+=instance.purchaseQuantityReceived
            stock.save()
        except Stock.DoesNotExist:
            stock.create(stockItem=instance.purchasePartId,location=instance.purchaseStock,minQty=0,aisle=0,row=0,bin=0,qtyOnHand=instance.purchaseQuantityReceived)
    else:
        try:
            stock=Stock.objects.get(stockItem=instance.purchasePartId,location=instance.purchaseStock)
            stock.qtyOnHand+=instance.purchaseQuantityReceived
            stock.save()
        except Stock.DoesNotExist:
            stock.create(stockItem=instance.purchasePartId,location=instance.purchaseStock,minQty=0,aisle=0,row=0,bin=0,qtyOnHand=instance.purchaseQuantityReceived)

#besiar mohem
###################################
@receiver(post_save, sender=WorkorderPart )
def save_WorkorderPart_profile(sender, instance, **kwargs):
    wo=WorkOrder.objects.get(id=instance.woPartWorkorder.id)
    woassetpart=AssetPart.objects.none()
    bom=BOMGroupPart.objects.none()
    try:
        woassetpart=AssetPart.objects.filter(assetPartAssetid=wo.woAsset,assetPartPid=instance.woPartStock.stockItem)
        if(woassetpart):
            print("yessss!!!!!!!!!!!!!!!!!!!")
        else:
            woassetpart.create(assetPartAssetid=wo.woAsset,assetPartPid=instance.woPartStock.stockItem,assetPartQnty=instance.woPartActulaQnty)

        #check bomgroup
    except woassetpart.DoesNotExist:
        try:
            # bomAsset=BOMGroupAsset.objects.filter(BOMGroupAssetAsset=wo.woAsset)
            print("123!!!!!!!!!!!!!!!!!!!!")
            woassetpart.create(assetPartAssetid=wo.woAsset,assetPartPid=instance.woPartStock.stockItem,assetPartQnty=instance.woPartActulaQnty)
        except:
            pass





#######################################



@receiver(post_save, sender=WorkOrder )
def save_wo_profile(sender, instance, **kwargs):


    try:
        if(instance==None):
            pass
            # print(created)
            # print(instance.assignedToUser)
            # Mail.SendNewSysMessage(instance.assignedToUser,instance.summaryofIssue ,instance.woPriority)
        else:
            if(instance.isScheduling==False):
                userlist=WorkorderUserNotification.objects.filter(woNotifWorkorder=instance)
                for c in userlist:
                    if(instance.isUpdating==False):
                            Mail.SendNewSysMessage(c,instance.summaryofIssue ,priority=instance.woPriority,msgid=instance.id,wo=instance)
                            # print("yuha!!!!!!!")
                    else:
                        # print("message is created")

                        Mail.SendUpdatedSysMessage(c,instance.summaryofIssue ,priority=instance.woPriority,msgid=instance.id)

                if(instance.assignedToUser):
                    # print(instance.assignedToUser)
                    Mail.SendUpdatedSysMessage(instance.assignedToUser,instance.summaryofIssue ,priority=instance.woPriority,msgid=instance.id,wo=instance)

    except Exception as e1:
         print(e1)
         exc_type, exc_obj, tb = sys.exc_info()
         print(tb.tb_lineno)
         print("error in work order signals")






# @receiver(pre_save, sender=AssetMeterReading )
# def save_user_profile(sender, instance, **kwargs):
#           try:
#               print("kirekhar#############################")
#               ##### چک کردن فعال بودن swo ????????????
#               sche=Schedule.objects.filter(schAsset=instance.assetMeterLocation).filter(shMeterReadingMetrics=instance.assetMeterMeterReadingUnit)
#               for unit in sche:
#                  if(unit.shMeterNextVal!=None):
#                   if(instance.assetMeterMeterReading>=unit.shMeterNextVal and instance.assetMeterMeterReading<=unit.shMeterReadingEndBy and unit.workOrder.running==True):
#                       unit.shMeterNextVal=unit.shMeterReadingEvreyQnty+instance.assetMeterMeterReading
#                       create_wo(unit)
#                       unit.save()
#               sche1=Schedule.objects.filter(schAsset=instance.assetMeterLocation).filter(shMeterReadingWhenMetric=instance.assetMeterMeterReadingUnit)
#
#               for unit in sche1:
#                   if(unit.shMeterReadingHasTiming==False):
#                       if(unit.shMetricComparison==0):
#                           if(instance.assetMeterMeterReading>unit.shMeterReadingWhenQnty and unit.workOrder.running==True):
#                               create_wo(unit) #create wo
#                               #print("yeah instance.assetMeterMeterReading>unit.shMeterReadingWhenQnty ")
#                               unit.save()
#                       if(unit.shMetricComparison==1):
#                            if(instance.assetMeterMeterReading<unit.shMeterReadingWhenQnty):
#                                create_wo(unit) #create wo
#                                unit.save()
#           except Exception as e1:
#               print("asddsadsa#############################")
#               print(e1)
#               exc_type, exc_obj, tb = sys.exc_info()
#               print(tb.tb_lineno)
#               print("error in signals")
# @receiver(pre_save, sender=AssetEvent )
# def save_user_profile(sender, instance, **kwargs):
#     try:
#         print(instance.AssetEventEventId)
#         print(instance.AssetEventAssetId)
#         ev=Schedule.objects.filter(schEvent=instance.AssetEventEventId).filter(schAsset=instance.AssetEventAssetId)
#         for unit in ev:
#
#             #if(unit.workOrder.running==True):
#                 create_wo(unit)
#
#
#
#     except Exception as e:
#         print(e)
#         print("problem in assetevent signal")
# @receiver(post_save, sender=WorkOrder)
# def create_wo_profile(sender, instance, created, **kwargs):
#     if created:
#         print("yuha!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
