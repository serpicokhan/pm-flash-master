from cmms.models import Asset,EquipSetting,AssetLife
from cmms.business.EquipSettingUtility import *
from cmms.business.EquipCostSettingUtility import *
from cmms.business.taskUtility import *
from cmms.business.PartUtility import *
from cmms.business.misccost import *
import jdatetime
import datetime
import json
from django.db.models import Q
from django.core.paginator import *
from django.db.models import Count

class AssetUtility:

    @staticmethod
    def getListAssetLastWeek():
        lastweek=Asset.objects.raw("select id,summaryofIssue,woPriority,woAsset_id,assignedToUser_id,woStatus,maintenanceType_id,completedByUser_id,estimatedLabor,actualLabor from workorder where isScheduling=0 and pmonth(CURRENT_DATE)=pmonth(datecreated) and ceil(pday(datecreated)/7)=ceil(pday(CURRENT_DATE)/7) and visibile=1 order by id desc")
        return lastweek
    @staticmethod
    def getListAssetLastMonth():
        lastmonth=Asset.objects.raw("select id,summaryofIssue,woPriority,woAsset_id,assignedToUser_id,woStatus,maintenanceType_id,completedByUser_id,estimatedLabor,actualLabor from workorder where isScheduling=0 and  pmonth(CURRENT_DATE)=pmonth(datecreated) and visibile=1 order by id desc")
        return lastmonth
    @staticmethod
    def getlastAsset():
        company=Asset.objects.filter(datecreated=datetime.date.today()).filter(isScheduling=False).filter(visibile=True).order_by("-id")
        return company
    # Generate paging
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
    ###############################################################


    @staticmethod
    def getEquipmentDownTime(start,end):
        eqList=list(EquipCostSettingUtility.getList())
        # print(''' select sum(TIMESTAMPDIFF(HOUR,cast(concat(assetOfflineFrom, ' ', assetOfflineFromTime) as datetime),cast(concat(assetOnlineFrom, ' ', assetOnlineFromTime) as datetime))) as id,
        #                       assetLifeAssetid_id,assetname
        #                       from assetlife  as t1
        #                       inner join assets on assets.id=t1.assetLifeAssetid_id
        #
        #                       where assetLifeAssetid_id in ({0}) and (assetOfflineFrom between '{1}' and '{2}')
        #                       and assetonlinestatus is not null
        #
        #                        group by assetLifeAssetid_id
        #                        '''.format(",".join(str(x) for x in eqList),start,end))
        return AssetLife.objects.raw(''' select sum(TIMESTAMPDIFF(HOUR,cast(concat(assetOfflineFrom, ' ', assetOfflineFromTime) as datetime),cast(concat(assetOnlineFrom, ' ', assetOnlineFromTime) as datetime))) as id,
                              assetLifeAssetid_id,assetname
                              from assetlife  as t1
                              inner join assets on assets.id=t1.assetLifeAssetid_id

                              where assetLifeAssetid_id in ({0}) and (assetOfflineFrom between '{1}' and '{2}') and assetonlinestatus is not null

                               group by assetLifeAssetid_id
                               '''.format(",".join(str(x) for x in eqList),start,end))
        # select sum(timediff(cast(concat(assetOnlineFrom, ' ', assetOnlineFromTime) as datetime),
        #                       cast(concat(assetOfflineFrom, ' ', assetOfflineFromTime) as datetime))),
        #                       cast(concat(assetOnlineFrom, ' ', assetOnlineFromTime) as datetime),
        #                       cast(concat(assetOfflineFrom, ' ', assetOfflineFromTime) as datetime),assetLifeAssetid_id
        #                       where assetLifeAssetid_id in ({0})
        #                        from assetlife
        #                        group by assetLifeAssetid_id
    @staticmethod
    def getEquipmentCost(start,end):
        eqList=list(EquipCostSettingUtility.getListByName())
        print(eqList)
        n1=0
        d={}
        for r1 in eqList:
            p1=PartUtility.getPartCostForAsset(r1.settingEqAsset.id,start,end)[0].id
            p2=ExtraCost.getMiscCostForAsset(r1.settingEqAsset.id,start,end)[0].id
            p3=TaskUtility.getAssetTimeCostByResource(r1.settingEqAsset.id,start,end)[0].id
            # print("!@!@!@@!")
            print(p1,p2,p3)
            if(not p1):
                n1+=0
            else:
                n1+=p1
            if(not p2):
                    n1+=0
            else:
                    n1+=p2
            if(not p3):
                    n1+=0
            else:
                    n1+=p3
            d[r1.settingEqAsset.assetName]=n1
            n1=0



        return d
    @staticmethod
    def getDashIstgahStatus(start,end):
        eqList=list(AssetTypeUtility.getList())

        n1=0
        d={}
        mval={}#corresponding maintenance value for eash station
        mcol={}
        mid=MaintenanceType.objects.all().exclude(id=1)
        assetname=[]
        for m in mid:
            mval[m.name]=[]
            mcol['{0}-1'.format(m.name)]=m.color

            for r1 in eqList:



                mval[m.name].append(Tasks.objects.raw("""select
                floor(COALESCE(sum(timestampdiff(minute,cast(concat(taskStartDate, ' ', taskStartTime) as datetime),
                cast(concat(taskDateCompleted, ' ', taskTimeCompleted) as datetime))),0)/60) as id from tasks

                 inner JOIN workorder on tasks.workOrder_id=workorder.id
                 inner join assets on workorder.woAsset_id=assets.id

                 where workorder.maintenanceType_id={0}
                 and tasks.taskStartDate between '{1}' and '{2}'
                 and assets.assetCategory_id={3} and workorder.isScheduling=0
                 ;


                """.format(m.id,start,end,r1.settingEqAsset.id))[0].id)


        mval["EM"]=[]
        mcol['EM-1']='red'

        for r1 in eqList:
            assetname.append(r1.settingEqAsset.name)


            mval["EM"].append(Tasks.objects.raw(""" select floor(COALESCE(sum(timestampdiff(minute,cast(concat(taskStartDate,
            ' ', taskStartTime) as datetime),
            cast(concat(taskDateCompleted, ' ', taskTimeCompleted) as datetime))),0)/60) as id from tasks

             inner JOIN workorder on tasks.workOrder_id=workorder.id
             inner join assets on workorder.woAsset_id=assets.id

             where  tasks.taskStartDate between '{0}' and '{1}'
             and assets.assetCategory_id={2} and workorder.isScheduling=0 and workorder.isem=1
             ;


            """.format(start,end,r1.settingEqAsset.id))[0].id)







        return mval,mcol,assetname;
        #gethumancostforwo(start,end)
    @staticmethod
    def getCategory():
        a=AssetCategory.objects.all()
        b=[]
        links=[]
        for item in a:
            b.append((item.isPartOf.id if item.isPartOf else -1,item.id,item.name))
        print(b)
        # parents, children = zip(*b)
        # root_nodes = {x for x in parets if x not in children}
        # for node in root_nodes:
        #     links.append(('Root', node))

        tree = AssetUtility.get_nodes((-2,-1,'همه'),b)
        return json.dumps(tree, indent=4)

    @staticmethod
    def getLocationCategory():
        a=Asset.objects.filter(assetTypes=1)
        b=[]
        links=[]
        for item in a:
            b.append((item.assetIsPartOf.id if item.assetIsPartOf else -1,item.id,item.assetName))
        print(b)
        # parents, children = zip(*b)
        # root_nodes = {x for x in parets if x not in children}
        # for node in root_nodes:
        #     links.append(('Root', node))

        tree = AssetUtility.get_nodes((-2,-1,'همه'),b)
        return json.dumps(tree, indent=4)

    @staticmethod
    def get_nodes(node,links):
        # print(node)
        d = {}
        d['text'] = str(node[2])
        d['href']="#"+d['text']
        d['tags']=str(node[1])
        children = AssetUtility.get_children(node,links)
        if children:
            d['nodes'] = [AssetUtility.get_nodes(child,links) for child in children]
        return d
    @staticmethod
    def get_children(node,links):
        #print(node[1],"))))))))))node")
        c=[x for x in links if x[0] == node[1]]
        return c
    @staticmethod
    def getAssetListByNameAndLocation(assetCatListId,LocationListId):
        wos=[]
        print(assetCatListId,"####################")
        if(len(assetCatListId)>0):
            wos=Asset.objects.filter(assetCategory__in=assetCatListId)
        elif(len(LocationListId)):
            wos=Asset.objects.filter(Q(id__in=LocationListId)|Q(assetIsLocatedAt__in=LocationListId)|Q(assetIsPartOf__in=LocationListId)).order_by('assetCategory__name','assetName')
        else:
            return Asset.objects.all().order_by('assetCategory__name','assetName')


        return wos

        #making where clause query
        # print(LocationListId,"$$$$$$$")
        # whereStr='1=1 '
        # if(assetCatListId!='-1'):
        #     #return Asset.objects.all()
        #     whereStr+="and assetcategory.id in ({0}) ".format(assetCatListId)
        # if(LocationListId!='-1'):
        #     #return Asset.objects.filter(assetIsLocatedAt__in=assetCatListId)
        #
        #     whereStr+="and assetIsLocatedAt_id in ({0})".format(LocationListId)
        # print("""select `assetName` as id,`assetCode`,assetcategory.name as catname,`assetManufacture`,`assetModel`,
        #                             `assetSerialNumber`,`assetStatus` from assets
        #                             inner join assetcategory on assets.assetCategory_id=assetcategory.id where {0} """.format(whereStr))
        # return Asset.objects.raw("""select `assetName` as id,`assetCode`,assetcategory.name as catname,`assetManufacture`,`assetModel`,
        #                             `assetSerialNumber`,`assetStatus` from assets
        #                             inner join assetcategory on assets.assetCategory_id=assetcategory.id where {0} """.format(whereStr))
    @staticmethod
    def getAssetListByCategory(assetCatListId):
            print(assetCatListId)
            # whereStr='1=1 '
            # if(assetCatListId!='-1'):
            #     return Asset.objects.filter(assetCategory__in=(assetCatListId)).values_list('id',flat=True)
            #     whereStr+="and assetcategory_id in ({0}) ".format(assetCatListId)
            # return Asset.objects.values_list('id',flat=True)
            if(len(assetCatListId)>0):
                return Asset.objects.filter(Q(assetCategory__in=assetCatListId)|Q(assetIsPartOf__assetCategory__in=assetCatListId)|Q(assetIsLocatedAt__assetCategory__in=assetCatListId)).values_list('id',flat=True)
            else:
                return Asset.objects.all().values_list('id',flat=True)

    @staticmethod
    def getOfflineCountByEvent(assetList,date1,date2):

            return AssetLife.objects.raw(''' select count(assetlife.id) as id,b.id as event,b.name as eventname
                                        from assetlife
                                        left join offlinestatus b on assetlife.assetofflinestatus_id=b.id

                                        where assetLifeAssetid_id in {0} and
                                        (assetOfflineFrom between "{1}" and "{2}")
                                        and assetlife.assetOnlineStatus is not null
                                        group by b.id



                                         '''.format(tuple(assetList),date1,date2))
            # print(AssetLife.objects.filter(assetOfflineFrom__range=(date1, date2),assetLifeAssetid__in=assetList).values('assetOfflineStatus').order_by().annotate(Count('id')).query,'##@#@!#!@#@!')
            # return AssetLife.objects.filter(assetOfflineFrom__range=(date1, date2),assetLifeAssetid__in=assetList).values('assetOfflineStatus').order_by().annotate(Count('id'))
    @staticmethod
    def getOfflineSumTimeByEvent(assetList,date1,date2):
            return AssetLife.objects.raw(''' select sum(timestampdiff(HOUR,
                                  cast(concat(assetOfflineFrom, ' ', assetOfflineFromTime) as datetime),cast(concat(assetOnlineFrom, ' ', assetOnlineFromTime) as datetime))) as id,b.id as eventid, b.name as eventname

                                  from assetlife  as t1


                                  inner join offlinestatus b on t1.assetofflinestatus_id=b.id

                                  where assetLifeAssetid_id in {0} and (assetOfflineFrom between '{1}' and '{2}')
                                  and
                                   t1.assetOnlineStatus is not null

                                   group by b.id
                                   '''.format(tuple(assetList),date1,date2))
    @staticmethod
    def getOfflineSumForAll(date1,date2):
            return AssetLife.objects.raw(''' select sum(timestampdiff(HOUR,
                                  cast(concat(assetOfflineFrom, ' ', assetOfflineFromTime) as datetime),
                                  cast(concat(assetOnlineFrom, ' ', assetOnlineFromTime) as datetime))) as id,
                                  from assetlife  as t1
                                  inner join assets c on t1.assetLifeAssetid_id=c.id
                                  where assetLifeAssetid_id in {0} and (assetOfflineFrom between '{1}' and '{2}')
                                  and t1.assetOnlineStatus is not null

                                   group by c.id
                                   '''.format(assetList,date1,date2))
    @staticmethod
    def getLabourHoursByAsset(date1,date2,assetCategory,mainType):
        #############$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        #add extra function for empty maintype
        whereConition=" where 1=1 "

        # if(len(mainType)>0):
        #     whereConition+=" and  maintenanceType_id in {0}".format(str(mainType))
        if(len(assetCategory)>0):
            whereConition+=" and  assetCategory_id in {0}".format(str(assetCategory))
        print("""  select id,get_task_asset_time_spent (id,'{0}','{1}','{2}') as timespent from assets {3} """.format(date1,date2,mainType,whereConition))
        return Asset.objects.raw("""  select id,get_task_asset_time_spent (id,'{0}','{1}','{2}') as timespent from assets {3}  """.format(date1,date2,mainType,whereConition))
    @staticmethod
    def getLabourHoursByAssetTop10(date1,date2,assetCategory,mainType):
        #############$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        #add extra function for empty maintype
        whereConition=" where 1=1 "

        # if(len(mainType)>0):
        #     whereConition+=" and  maintenanceType_id in {0}".format(str(mainType))
        if(len(assetCategory)>0):
            whereConition+=" and  assetCategory_id in {0}".format(str(assetCategory))
        # print("""  select id,get_task_asset_time_spent (id,'{0}','{1}','{2}') as timespent from assets {3} order by timespent desc limit 10 COALESCE""".format(date1,date2,mainType,whereConition))

        return Asset.objects.raw("""  select id,get_task_asset_time_spent (id,'{0}','{1}','{2}') as timespent from assets {3} order by timespent desc limit 10 """.format(date1,date2,mainType,whereConition))
############# search Asset in assetlist.html
    @staticmethod
    def seachAsset(assType,searchStr):

        aType=0
        if(assType=='Location'):
            aType=1
        elif(assType=='Machine'):
            aType=2
        elif(assType=='Tool'):
            aType=3
        else:
            #All type
            aType=0
         # print("43 partutility$$$$$$$$$$$$$$$$$$$")
         # print("select id from parts where (partname like '%{}%') or (partDescription like '%{}%') or (partcode like '%{}%') or (partModel like '%{}%') order by id desc".format(searchStr,searchStr,searchStr,searchStr))
        if(searchStr != 'empty'):
             if(aType>0):
                 if(searchStr.isdigit()):
                     return Asset.objects.filter(Q(assetName__contains=searchStr,assetTypes=aType)|Q(assetCode__contains=searchStr,assetTypes=aType)|Q(id=int(searchStr),assetTypes=aType)) #raw("select id from parts where (partname like '\%@p\%') or (partDescription like 'p') or (partcode like 'p') or (partModel like 'p') order by id desc")
                 return Asset.objects.filter(assetName__contains=searchStr,assetTypes=aType)|Asset.objects.filter(assetCode__contains=searchStr,assetTypes=aType) #raw("select id from parts where (partname like '\%@p\%') or (partDescription like 'p') or (partcode like 'p') or (partModel like 'p') order by id desc")
             else:
                 if(searchStr.isdigit()):
                      return Asset.objects.filter(Q(assetName__contains=searchStr)|Q(assetCode__contains=searchStr)|Q(id=int(searchStr))) #raw("select id from parts where (partname like '\%@p\%') or (partDescription like 'p') or (partcode like 'p') or (partModel like 'p') order by id desc")
                 return Asset.objects.filter(assetName__contains=searchStr)|Asset.objects.filter(assetCode__contains=searchStr) #raw("select id from parts where (partname like '\%@p\%') or (partDescription like 'p') or (partcode like 'p') or (partModel like 'p') order by id desc")

         # return WorkOrder.objects.filter(summaryofIssue__isnull=False,isScheduling=False,woTags__contains=searchStr).order_by('-id')
        else:
             if(aType>0):
                 return Asset.objects.filter(assetTypes=aType).order_by('-id')
             else:
                 return Asset.objects.all().order_by('-id')
    @staticmethod
    def getAssetOfflineStatus(id):
        n1=AssetLife.objects.raw(""" select (count(assetlife.id)/total_getdownhits({0}))*100   as id ,offlinestatus.name as reason  from assetlife inner join offlinestatus on assetlife.assetOfflineStatus_id=offlinestatus.id inner join assets on assets.id=assetlife.assetLifeAssetid_id  where (assetlifeassetid_id={0} or assets.assetIsLocatedAt_id={0} or assets.assetIsPartOf_id={0}) group by assetofflinestatus_id """.format(id))
        return n1
    @staticmethod
    def getAssetOfflineStatusLine(id):
        n1=AssetLife.objects.raw(""" select count(assetlife.id) as id,pmonth(assetofflinefrom) as month from assetlife inner join assets on assets.id=assetlife.assetlifeassetid_id where (assets.assetIsLocatedAt_id={0} or assetlifeassetid_id={0} or assets.assetIsPartOf_id={0}) and pyear(CURRENT_DATE)=pyear(assetOfflineFrom) group by(pmonth(assetofflinefrom))  """.format(id))
        return n1
    @staticmethod
    def getAssetOfflineHistory(assetId,assetCode,date1,date2):
        # print(assetCode)
        wos=[]
        assetlifes=[]
        wos=AssetLife.objects.filter(assetLifeAssetid=assetId,assetOfflineFrom__range=[date1,date2])
        # print(AssetLife.objects.filter(assetLifeAssetid__assetStatus=False).query)
        # wos=AssetLife.objects.filter(assetLifeAssetid__assetStatus=False)
        if(len(assetCode)>0):
            # print(wos.filter(assetStopCode__in=assetCode).query)
            wos=wos.filter(assetStopCode__in=assetCode)
            # print(wos.filter(assetStopCode__in=assetCode).query)
        return wos
    @staticmethod
    def getAssetOfflineTime(date1,date2):
        # print("select  COALESCE( sum(timestampdiff(minute,cast(concat(assetOfflineFrom, ' ', assetOfflineFromTime) as datetime),cast(concat(assetOnlineFrom, ' ', assetOnlineFromTime) as datetime))),0)  as id from assetlife where assetOfflineFrom between '{0}' and '{1}' ".format(date1,date2))
        wos=AssetLife.objects.raw("select  COALESCE( sum(timestampdiff(minute,cast(concat(assetOfflineFrom, ' ', assetOfflineFromTime) as datetime),cast(concat(assetOnlineFrom, ' ', assetOnlineFromTime) as datetime))),0)  as id from assetlife where assetOfflineFrom between '{0}' and '{1}' ".format(date1,date2))


        return wos[0].id/60

    @staticmethod
    def createNewAssetStatus(wo):
        product=0

        if(wo.woStatus in (7,8,9)):
            dt1=datetime.datetime.combine(wo.datecreated,wo.timecreated)
            dt2=datetime.datetime.combine(wo.dateCompleted,wo.timeCompleted)
            product=(dt2-dt1).total_seconds()/3600
            AssetLife.objects.create(assetLifeAssetid=wo.woAsset,assetOfflineFrom=wo.datecreated,assetOfflineFromTime=wo.timecreated,assetSetOfflineByUser=wo.assignedToUser,assetWOAssoc=wo,assetOnlineFrom=wo.dateCompleted,assetOnlineFromTime=wo.timeCompleted,assetSetOnlineByUser=wo.assignedToUser,assetOnlineStatus=0,assetStopCode=wo.woStopCode,assetOnlineProducteHourAffected=product)
        else:
            AssetLife.objects.create(assetLifeAssetid=wo.woAsset,assetOfflineFrom=wo.datecreated,assetOfflineFromTime=wo.timecreated,assetSetOfflineByUser=wo.assignedToUser,assetWOAssoc=wo,assetStopCode=wo.woStopCode)
            wo.woAsset.assetState=False;
            wo.woAsset.save()
    @staticmethod
    def updateAssetLife(wo):
        assetlife=AssetLife.objects.filter(assetWOAssoc=form.instance)
        if(assetlife):
            for i in assetlife:
                if(wo.woStatus in (7,8,9)):
                    dt1=datetime.datetime.combine(wo.datecreated,wo.timecreated)
                    dt2=datetime.datetime.combine(wo.dateCompleted,wo.timeCompleted)
                    product=(dt2-dt1).total_seconds()/3600
                    AssetLife.objects.create(assetLifeAssetid=wo.woAsset,assetOfflineFrom=wo.datecreated,assetOfflineFromTime=wo.timecreated,assetSetOfflineByUser=wo.assignedToUser,assetWOAssoc=wo,assetOnlineFrom=wo.dateCompleted,assetOnlineFromTime=wo.timeCompleted,assetSetOnlineByUser=wo.assignedToUser,assetOnlineStatus=0,assetStopCode=wo.woStopCode,assetOnlineProducteHourAffected=product)
                else:
                    AssetLife.objects.create(assetLifeAssetid=wo.woAsset,assetOfflineFrom=wo.datecreated,assetOfflineFromTime=wo.timecreated,assetSetOfflineByUser=wo.assignedToUser,assetWOAssoc=wo,assetStopCode=wo.woStopCode)
                    wo.woAsset.assetState=False;
                    wo.woAsset.save()
                i.delete()
