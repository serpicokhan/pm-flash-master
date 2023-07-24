from django.db.models.signals import pre_save,post_save,pre_delete
from django.dispatch import receiver
from cmms.models import *
from cmms.business.mail import Mail
import sys
from cmms.business.stockutility import *
from cmms.business.fcm import *
from django.core.exceptions import ObjectDoesNotExist
from pprint import pprint
from datetime import datetime
from cmms.tasks import some_function
# from asgiref.sync import sync_to_async
# from firebase_admin.messaging import Message
# from firebase_admin import messaging

def create_wo(unit):
    try:
        ##### Create Wo #########
        stableWo=WorkOrder.objects.get(id=unit.workOrder_id)
        oldWo=WorkOrder.objects.get(id=unit.workOrder_id)
        stableWo.pk=None
        stableWo.visibile=True
        stableWo.isScheduling=False
        stableWo.isPm=True
        stableWo.datecreated=datetime.now().date()
        stableWo.timecreated=datetime.now().time()
        stableWo.isPartOf=unit.workOrder
        # Newsch.schNextWo=WorkOrder.objects.create(datecreated=Newsch.schnextTime.date(),timecreated=Newsch.schnextTime.time(),visibile=False,isScheduling=False,isPartOf=Newsch.workOrder)
        stableWo.save()

        #################
        # wt=WorkorderTask.objects.filter(workorder=oldWo)
        wt=Tasks.objects.filter(workOrder=oldWo)
        if(wt!=None):
            for f in wt:
                f.pk=None
                f.workorder=stableWo
                f.save()
        ##############
        wp=WorkorderPart.objects.filter(woPartWorkorder=oldWo)
        if(wp!=None):
            for f in wp:
                f.pk=None
                f.woPartWorkorder=stableWo
                woPartMsg=StockUtility.remove(f)
                f.save()
        ###############
        wf=WorkorderFile.objects.filter(woFileworkorder=oldWo)
        if(wf!=None):

            for f in wf:
                f.pk=None
                f.woFileworkorder=stableWo
                f.save()

        ################
        try:
            wn=get_object_or_404(WorkorderUserNotification,woNotifWorkorder=oldWo)
            if(wn!=None):
                wn.pk=None
                wn.woNotifWorkorder=stableWo
                wn.save()
        except:
            print("error wonotif")
    except Exception as ex:
        print(ex)
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
        except ObjectDoesNotExist:
            stock.create(stockItem=instance.purchasePartId,location=instance.purchaseStock,minQty=0,aisle=0,row=0,bin=0,qtyOnHand=instance.purchaseQuantityReceived)
    else:
        try:
            stock=Stock.objects.get(stockItem=instance.purchasePartId,location=instance.purchaseStock)
            stock.qtyOnHand+=instance.purchaseQuantityReceived
            stock.save()
        except ObjectDoesNotExist:
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
    except ObjectDoesNotExist:
        try:
            # bomAsset=BOMGroupAsset.objects.filter(BOMGroupAssetAsset=wo.woAsset)
            print("123!!!!!!!!!!!!!!!!!!!!")
            woassetpart.create(assetPartAssetid=wo.woAsset,assetPartPid=instance.woPartStock.stockItem,assetPartQnty=instance.woPartActulaQnty)
        except:
            pass





#######################################

async def make_book(*args, **kwargs):
    results = await sync_to_async(push_notification.send_push('AAAAClhesu0:','cZiRAQyARNKW5KPUmoMUmt:APA91bGKXvX8aZQwGrzu7w7OCj6W_a33WTfiMta4clGpTTyfjgWdEHVan8Zj-SUuPNFlJN8Etjehf-0odB2BgwEHFjh4cZN17iicPei0Jxa1xnahDxRlvPmaYj9w5Plxl3pPEVZ4Lts9','New Workorder', 'dsadsa'), thread_sensitive=True)(pk=123)
    return result

@receiver(post_save, sender=WorkOrder )
def save_wo_profile(sender, instance, **kwargs):
    # asyncio.run(make_book())
    # asyncio.run(some_function(instance.summaryofIssue))
    # some_function.delay('dsadsa')
    # push_notification.send_push('AAAAClhesu0:','cZiRAQyARNKW5KPUmoMUmt:APA91bGKXvX8aZQwGrzu7w7OCj6W_a33WTfiMta4clGpTTyfjgWdEHVan8Zj-SUuPNFlJN8Etjehf-0odB2BgwEHFjh4cZN17iicPei0Jxa1xnahDxRlvPmaYj9w5Plxl3pPEVZ4Lts9','New Workorder', 'dsadsa')


   #  data1={
   #      "Nick" : "Mario",
   #      "body" : "great match!",
   #      "Room" : "PortugalVSDenmark"
   # }
   #  message=messaging.MulticastMessage(notification=messaging.Notification(title='dasdsa',body='dasdsadas'),data=data1,tokens=['cZiRAQyARNKW5KPUmoMUmt:APA91bGKXvX8aZQwGrzu7w7OCj6W_a33WTfiMta4clGpTTyfjgWdEHVan8Zj-SUuPNFlJN8Etjehf-0odB2BgwEHFjh4cZN17iicPei0Jxa1xnahDxRlvPmaYj9w5Plxl3pPEVZ4Lts9'])
   #  messaging.send_multicast(message)
    try:

        print("thats done")
        if(instance==None):
            pass
            # print(created)
            # print(instance.assignedToUser)
            # Mail.SendNewSysMessage(instance.assignedToUser,instance.summaryofIssue ,instance.woPriority)
        else:
            # if(instance.isScheduling==False):
            #     userlist=WorkorderUserNotification.objects.filter(woNotifWorkorder=instance)
            #     for c in userlist:
            #
            #         if(instance.isUpdating==False):
            #
            #                 Mail.SendNewSysMessage(c.woNotifUser,instance.summaryofIssue ,priority=instance.woPriority,msgid=instance.id,wo=instance)
            #                 push_notification.sendpush('AIzaSyCXtTSMxPAxR7WsI_m5AAhfJWFdwd9QIxg','cZiRAQyARNKW5KPUmoMUmt:APA91bGKXvX8aZQwGrzu7w7OCj6W_a33WTfiMta4clGpTTyfjgWdEHVan8Zj-SUuPNFlJN8Etjehf-0odB2BgwEHFjh4cZN17iicPei0Jxa1xnahDxRlvPmaYj9w5Plxl3pPEVZ4Lts9','New Workorder','salame mojadad')
            #                 print("thats done!!!!!!!!!!!!!")
            #                 # print("yuha!!!!!!!")
            #         else:
            #             # print("message is created")
            #
            #
            #             Mail.SendUpdatedSysMessage(c.woNotifUser,instance.summaryofIssue ,priority=instance.woPriority,msgid=instance.id)
            #
            #     if(instance.assignedToUser):
            #         # print(instance.assignedToUser)
            #         Mail.SendUpdatedSysMessage(instance.assignedToUser,instance.summaryofIssue ,priority=instance.woPriority,msgid=instance.id,wo=instance)
            #         # user_token=push_notification.find_user_token(instance.assignedToUser.id)
            #         ########################################
            #         # if(user_token):
            #         #     push_notification.send_push(API_KEY,user_token
            #         #                            ,'دستور کار جدید',instance.summaryofIssue)
            user_token=SysUser.objects.get(id=instance.assignedToUser).token
            admin=SysUser.objects.get(id=1).token
            if(user_token):
                some_function.delay(user_token,instance.assignedToUser);
            some_function.delay(admin,instance.summaryOfIssue);

    except Exception as e1:
         print(e1)
         exc_type, exc_obj, tb = sys.exc_info()
         print(tb.tb_lineno)
         print("error in work order signals")




    # asyncio.run(some_function(instance.summaryofIssue))

@receiver(post_save, sender=AssetMeterReading )
def save_assetmeter(sender, instance, **kwargs):
          try:
              print("somthing happen")

              ##### چک کردن فعال بودن swo ????????????

              sche=Schedule.objects.filter(schAsset=instance.assetMeterLocation,shMeterReadingMetrics=instance.assetMeterMeterReadingUnit,workOrder__running=True,shMeterReadingHasTiming=True)

              for unit in sche:
                 if(unit.shMeterNextVal!=None):
                         if(instance.assetMeterMeterReading>=unit.shMeterNextVal  and unit.workOrder.running==True):
                          #and instance.assetMeterMeterReading<=unit.shMeterReadingEndBy

                          unit.shMeterNextVal=unit.shMeterReadingEvreyQnty+instance.assetMeterMeterReading
                          # unit.shMeterReadingStartAt=
                          create_wo(unit)
                          print("Hello")
                          unit.save()


              sche1=Schedule.objects.filter(schAsset=instance.assetMeterLocation,shMeterReadingWhenMetric=instance.assetMeterMeterReadingUnit,shMeterReadingHasTiming=False,workOrder__running=True)
              #
              for unit in sche1:

                      if(unit.shMetricComparison==0):
                          if(instance.assetMeterMeterReading>unit.shMeterReadingWhenQnty and unit.workOrder.running==True):
                              create_wo(unit) #create wo
                              #print("yeah instance.assetMeterMeterReading>unit.shMeterReadingWhenQnty ")
                              unit.save()
                      if(unit.shMetricComparison==1):
                           if(instance.assetMeterMeterReading<unit.shMeterReadingWhenQnty):
                               create_wo(unit) #create wo
                               unit.save()
          except Exception as e1:
              print("asddsadsa#############################")
              print(e1)
              exc_type, exc_obj, tb = sys.exc_info()
              print(tb.tb_lineno)
              print("error in signals Asset Meter Reading")

@receiver(post_save, sender=AssetEvent )
def save_asset_event(sender, instance, **kwargs):
    try:

        ev=Schedule.objects.filter(schEvent=instance.AssetEventEventId).filter(schAsset=instance.AssetEventAssetId)
        for unit in ev:

            if(unit.workOrder.running==True):
                create_wo(unit)
                # print(ev,"sarvi")



    except Exception as e:
        print(e)
        print("problem in assetevent signal")
# @receiver(post_save, sender=AssetMeterReading )
# def save_assetmeter_event(sender, instance, **kwargs):
#     try:
#
#         ev=AssetMeterReading.objects.filter(schEvent=instance.AssetEventEventId).filter(schAsset=instance.AssetEventAssetId)
#         for unit in ev:
#
#             if(unit.workOrder.running==True):
#                 create_wo(unit)
#                 # print(ev,"sarvi")
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
@receiver(pre_save, sender=BusinessPart )
def save_BusinessPart_event(sender, instance, **kwargs):
    if(instance.businessPartisDefault):
        BusinessPart.objects.filter(BusinessPartPart=instance.BusinessPartPart,businessPartisDefault=True).update(businessPartisDefault=False)
# @receiver(pre_delete, sender=Tasks)
# def delete_related(sender, instance, **kwargs):
#     wo = instance.workOrder # instance is your Purchase instance that is
#     if(wo.isScheduling==True):
#         wos=WorkOrder.objects.filter(isPartOf=wo,visibile=False)
#         tasks=Tasks.objects.filter(worOrder__in=wos)
#         for i in tasks:
#             i.delete()

    # about to be deleted
