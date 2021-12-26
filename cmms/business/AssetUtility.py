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
        mid=MaintenanceType.objects.all()
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
    def getDashIstgahStatusWithLocation(start,end,location):
        eqList=list(AssetTypeUtility.getList().filter(settingLocation__id=location))
        n1=0
        d={}
        mval={}#corresponding maintenance value for eash station
        mcol={}
        mid=MaintenanceType.objects.all()
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
                 and assets.assetCategory_id={3} and workorder.isScheduling=0 and assets.assetIsLocatedAt_id={4}
                 ;


                """.format(m.id,start,end,r1.settingEqAsset.id,location))[0].id)


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
             and assets.assetCategory_id={2} and workorder.isScheduling=0 and workorder.isem=1 and assets.assetIsLocatedAt_id={3}
             ;


            """.format(start,end,r1.settingEqAsset.id,location))[0].id)







        return mval,mcol,assetname;
        #gethumancostforwo(start,end)
    @staticmethod
    def getCategory():
        a=AssetCategory.objects.all()
        b=[]
        links=[]
        for item in a:
            b.append((item.isPartOf.id if item.isPartOf else -1,item.id,item.name))
        # print(b)
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
            # print("count")
            # print(''' select count(assetlife.id) as id,b.id as event,b.causeDescription as eventname
            #                             from assetlife
            #                             left join workorder wo on assetlife.assetWOAssoc_id=wo.id
            #                             left join causecode b on wo.woCauseCode_id=b.id
            #
            #                             where assetLifeAssetid_id in {0} and
            #                             (assetOfflineFrom between "{1}" and "{2}")
            #                             and assetlife.assetOnlineStatus is not null
            #                             group by b.id
            #
            #
            #
            #                              '''.format(tuple(assetList),date1,date2))

            return AssetLife.objects.raw(''' select count(assetlife.id) as id,b.id as event,b.causeDescription as eventname
                                        from assetlife
                                        left join workorder wo on assetlife.assetWOAssoc_id=wo.id
                                        left join causecode b on wo.woCauseCode_id=b.id

                                        where assetLifeAssetid_id in {0} and
                                        (assetOfflineFrom between "{1}" and "{2}")
                                        and assetlife.assetOnlineStatus is not null
                                        group by b.id



                                         '''.format(tuple(assetList),date1,date2))
            # print(AssetLife.objects.filter(assetOfflineFrom__range=(date1, date2),assetLifeAssetid__in=assetList).values('assetOfflineStatus').order_by().annotate(Count('id')).query,'##@#@!#!@#@!')
            # return AssetLife.objects.filter(assetOfflineFrom__range=(date1, date2),assetLifeAssetid__in=assetList).values('assetOfflineStatus').order_by().annotate(Count('id'))
    @staticmethod
    def getOfflineSumTimeByEvent(assetList,date1,date2):
            # print("sum")
            # print(''' select sum(timestampdiff(HOUR,
            #                       cast(concat(assetOfflineFrom, ' ', assetOfflineFromTime) as datetime),cast(concat(assetOnlineFrom, ' ', assetOnlineFromTime) as datetime))) as id,b.id as eventid, b.causeDescription as eventname
            #
            #                       from assetlife  as t1
            #
            #                         left join workorder wo on t1.assetWOAssoc_id=wo.id
            #                         left join causecode b on wo.woCauseCode_id=b.id
            #
            #                       where assetLifeAssetid_id in {0} and (assetOfflineFrom between '{1}' and '{2}')
            #                       and
            #                        t1.assetOnlineStatus is not null
            #
            #                        group by b.id
            #                        '''.format(tuple(assetList),date1,date2))
            return AssetLife.objects.raw(''' select sum(timestampdiff(HOUR,
                                  cast(concat(assetOfflineFrom, ' ', assetOfflineFromTime) as datetime),cast(concat(assetOnlineFrom, ' ', assetOnlineFromTime) as datetime))) as id,b.id as eventid, b.causeDescription as eventname

                                  from assetlife  as t1

                                    left join workorder wo on t1.assetWOAssoc_id=wo.id
                                    left join causecode b on wo.woCauseCode_id=b.id

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
        whereConition="left join workorder as wo on wo.woasset_id=assets.id  where wo.maintenanceType_id in ({0})".format(mainType)

        # if(len(mainType)>0):
        #     whereConition+=" and  maintenanceType_id in {0}".format(str(mainType))
        if(len(assetCategory)>0):
            whereConition+=" and  assetCategory_id in {0}".format(str(assetCategory))
        # print(""" select distinct(assets.id),get_task_asset_time_spent2 (assets.id,'{0}','{1}') as timespent from assets {2}  """.format(date1,date2,whereConition))
        return Asset.objects.raw(""" select distinct(assets.id),get_task_asset_time_spent2 (assets.id,'{0}','{1}') as timespent from assets {2}  """.format(date1,date2,whereConition))
    @staticmethod
    def getLabourHoursByAssetTop10(date1,date2,assetCategory,mainType):
        #############$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        whereConition="left join workorder as wo on wo.woasset_id=assets.id  where wo.maintenanceType_id in ({0})".format(mainType)

        # if(len(mainType)>0):
        #     whereConition+=" and  maintenanceType_id in {0}".format(str(mainType))
        if(len(assetCategory)>0):
            whereConition+=" and  assetCategory_id in {0}".format(str(assetCategory))
        # print(""" select distinct(assets.id),get_task_asset_time_spent2 (assets.id,'{0}','{1}') as timespent from assets {2}  """.format(date1,date2,whereConition))
        return Asset.objects.raw(""" select distinct(assets.id),get_task_asset_time_spent2 (assets.id,'{0}','{1}') as timespent from assets {2} order by timespent desc limit 10  """.format(date1,date2,whereConition))

        # return Asset.objects.raw("""  select id,get_task_asset_time_spent (id,'{0}','{1}','{2}') as timespent from assets {3} order by timespent desc limit 10 """.format(date1,date2,mainType,whereConition))
############# search Asset in assetlist.html
    @staticmethod
    def seachAsset(assType,searchStr):


        aType=0
        if(assType=='1'):
            aType=1
        elif(assType=='2'):
            aType=2
        elif(assType=='3'):
            aType=3
        else:
            #All type
            aType=0
        result=Asset.objects.all()


        if(searchStr != 'empty'):
            q=searchStr
            for qstr in q:
                if(aType>0):
                     if(qstr.isdigit()):
                         result = result.filter(Q(assetName__icontains=qstr,assetTypes=aType)
                                                |Q(assetCode__icontains=qstr,assetTypes=aType)|Q(id=int(qstr),assetTypes=aType)|Q(assetCategory__name__icontains=qstr,assetTypes=aType)).order_by('-id')
                     else:
                        print("here")

                        result= result.filter(Q(assetName__icontains=qstr,assetTypes=aType)|Q(assetCode__icontains=qstr,assetTypes=aType)
                                           |Q(assetCategory__name__icontains=qstr,assetTypes=aType)).order_by('-id')
                else:
                     if(qstr.isdigit()):
                          result= result.filter(Q(assetName__icontains=qstr)|Q(assetCode__icontains=qstr)|Q(id=int(qstr))).order_by('-id')
                     else:
                         result= result.filter(Q(assetName__icontains=qstr)|Q(assetCode__icontains=qstr)|Q(assetCategory__name__icontains=qstr)).order_by('-id')
            return result.extra(select={'length':'Length(assetName)'}).order_by('length')


         # return WorkOrder.objects.filter(summaryofIssue__isnull=False,isScheduling=False,woTags__contains=searchStr).order_by('-id')
        else:
             if(aType>0):
                 print(aType,'$$$$$')
                 return result.filter(assetTypes=aType).order_by('-id')
             else:
                 return result.extra(select={'length':'Length(assetName)'}).order_by('length')
    @staticmethod
    def seachAsset2(searchStr,asset_loc=0,asset_cat=0):


        aType=0
        assType=0
        if(assType=='1'):
            aType=1
        elif(assType=='2'):
            aType=2
        elif(assType=='3'):
            aType=3
        else:
            #All type
            aType=0
        result=Asset.objects.all()


        if(searchStr != ''):
            q=searchStr
            for qstr in q:
                if(aType>0):
                     if(qstr.isdigit()):
                         result = result.filter(Q(assetName__icontains=qstr,assetTypes=aType)
                                                |Q(assetCode__icontains=qstr,assetTypes=aType)|Q(id=int(qstr),assetTypes=aType)|Q(assetCategory__name__icontains=qstr,assetTypes=aType)).order_by('-id')
                     else:

                        result= result.filter(Q(assetName__icontains=qstr,assetTypes=aType)|Q(assetCode__icontains=qstr,assetTypes=aType)
                                           |Q(assetCategory__name__icontains=qstr,assetTypes=aType)).order_by('-id')
                else:
                     if(qstr.isdigit()):
                          result= result.filter(Q(assetName__icontains=qstr)|Q(assetCode__icontains=qstr)|Q(id=int(qstr))).order_by('-id')
                     else:
                         result= result.filter(Q(assetName__icontains=qstr)|Q(assetCode__icontains=qstr)|Q(assetCategory__name__icontains=qstr)).order_by('-id')
            return result.extra(select={'length':'Length(assetName)'}).order_by('length')


         # return WorkOrder.objects.filter(summaryofIssue__isnull=False,isScheduling=False,woTags__contains=searchStr).order_by('-id')
        else:
             if(aType>0):
                 print(aType,'$$$$$')
                 return result.filter(assetTypes=aType).order_by('-id')
             else:
                 return result.extra(select={'length':'Length(assetName)'}).order_by('length')
    @staticmethod
    def getAssetOfflineStatus(id):
        n1=AssetLife.objects.raw(""" select (count(assetlife.id)/total_getdownhits({0}))*100   as id ,b.causeDescription as reason,b.causeCode  from assetlife
         left join workorder wo on assetlife.assetWOAssoc_id=wo.id
         left join causecode b on wo.woCauseCode_id=b.id
         inner join assets on assets.id=assetlife.assetLifeAssetid_id
         where (assetlifeassetid_id={0} or assets.assetIsLocatedAt_id={0} or assets.assetIsPartOf_id={0})
         group by b.causeCode  """.format(id))
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
    def getAssetOfflineTime2(date1,date2,loc):
        # print("select  COALESCE( sum(timestampdiff(minute,cast(concat(assetOfflineFrom, ' ', assetOfflineFromTime) as datetime),cast(concat(assetOnlineFrom, ' ', assetOnlineFromTime) as datetime))),0)  as id from assetlife where assetOfflineFrom between '{0}' and '{1}' ".format(date1,date2))
        wos=AssetLife.objects.raw("""select  COALESCE( sum(timestampdiff(minute,cast(concat(assetOfflineFrom, ' '
        , assetOfflineFromTime) as datetime),cast(concat(assetOnlineFrom, ' ', assetOnlineFromTime) as datetime))),0)
         as id from assetlife
         inner join assets on assets.id=assetlife.assetLifeAssetid_id


          where (assetOfflineFrom between '{0}' and '{1}') and assets.assetIsLocatedAt_id={2} """.format(date1,date2,loc))


        return wos[0].id/60

    @staticmethod
    def createNewAssetStatus(wo):
        product=0

        if(wo.woStatus in (7,8,9)):
            dt1=datetime.datetime.combine(wo.datecreated,wo.timecreated)
            dt2=datetime.datetime.combine(wo.dateCompleted,wo.timeCompleted)
            product=(dt2-dt1).total_seconds()/3600
            AssetLife.objects.create(assetLifeAssetid=wo.woAsset,assetOfflineFrom=wo.datecreated,assetOfflineFromTime=wo.timecreated,assetSetOfflineByUser=wo.assignedToUser,assetWOAssoc=wo,assetOnlineFrom=wo.dateCompleted,assetOnlineFromTime=wo.timeCompleted,assetSetOnlineByUser=wo.assignedToUser,assetOnlineStatus=0,assetStopCode=wo.woStopCode,assetOnlineProducteHourAffected=product,assetCauseCode=wo.woCauseCode)
        else:
            AssetLife.objects.create(assetLifeAssetid=wo.woAsset,assetOfflineFrom=wo.datecreated,assetOfflineFromTime=wo.timecreated,assetSetOfflineByUser=wo.assignedToUser,assetWOAssoc=wo,assetStopCode=wo.woStopCode,assetCauseCode=wo.woCauseCode)
            # wo.woAsset.assetState=False;
            wo_ass=wo.woAsset
            wo_ass.assetState=False;
            wo_ass.save()
    @staticmethod
    def updateAssetLife(wo):
        assetlife=AssetLife.objects.filter(assetWOAssoc=wo)
        if(assetlife):
            for i in assetlife:
                if(wo.woStatus in (7,8,9)):
                    dt1=datetime.datetime.combine(wo.datecreated,wo.timecreated)
                    dt2=datetime.datetime.combine(wo.dateCompleted,wo.timeCompleted)
                    product=(dt2-dt1).total_seconds()/3600
                    AssetLife.objects.create(assetLifeAssetid=wo.woAsset,assetOfflineFrom=wo.datecreated,assetOfflineFromTime=wo.timecreated,assetSetOfflineByUser=wo.assignedToUser,assetWOAssoc=wo,assetOnlineFrom=wo.dateCompleted,assetOnlineFromTime=wo.timeCompleted,assetSetOnlineByUser=wo.assignedToUser,assetOnlineStatus=0,assetStopCode=wo.woStopCode,assetOnlineProducteHourAffected=product,assetCauseCode=wo.woCauseCode)
                else:
                    AssetLife.objects.create(assetLifeAssetid=wo.woAsset,assetOfflineFrom=wo.datecreated,assetOfflineFromTime=wo.timecreated,assetSetOfflineByUser=wo.assignedToUser,assetWOAssoc=wo,assetStopCode=wo.woStopCode,assetCauseCode=wo.woCauseCode)
                    wo_ass=wo.woAsset
                    wo_ass.assetState=False;
                    wo_ass.save()
                i.delete()
        else:
            if(wo.woStopCode):
                AssetUtility.createNewAssetStatus(wo)


    @staticmethod
    def GetOnTimeCompletedWONumByAsset(start,end,asset,maintype):

        return WorkOrder.objects.raw("select count(id) as id from workorder where datecompleted <= requiredCompletionDate and (datecompleted between '{0}' and '{1}') and  wostatus=7 and woAsset_id={2} and maintenanceType_id={3}".format(start,end,asset,maintype))
    ##########
    @staticmethod
    def GetTotalCompletedWONumByAsset(start,end,asset,maintype):
        return WorkOrder.objects.raw("select count(id) as id from workorder where  (datecompleted between '{0}' and '{1}') and  wostatus=7 and woAsset_id={2} and maintenanceType_id={3}".format(start,end,asset,maintype))
    #########################################################################################
    @staticmethod
    def GetOnTimeCompletedWONumByAsset2(start,end,asset):

        return WorkOrder.objects.raw("select count(id) as id from workorder where datecompleted <= requiredCompletionDate and (datecompleted between '{0}' and '{1}') and  wostatus=7 and woAsset_id={2}".format(start,end,asset))

    #################
    #########################################################################################
    @staticmethod
    def GetTotalCompletedWONumByAsset2(start,end,asset):
        return WorkOrder.objects.raw("select count(id) as id from workorder where  (datecompleted between '{0}' and '{1}') and  wostatus=7 and woAsset_id={2} ".format(start,end,asset))


    #########################################################################################
    @staticmethod
    def GetDowntimeByAsset(start,end,assetid):
        # print("select count(assetlife.id) as id,s.stopDescription as d2,assetStopCode_id from assetlife left join StopCode as s on assetlife.assetStopCode_id=s.id where  (assetOfflineFrom between '{0}' and '{1}') and assetSetOfflineByUser_id={2} group by assetStopCode_id".format(start,end,userid))
        # print("select sum(timestampdiff(MINute,cast(concat(assetOfflineFrom, ' ', assetOfflineFromTime) as datetime),cast(concat(assetOnlineFrom, ' ',assetOnlineFromTime) as datetime))) as id,s.stopDescription as d2,assetStopCode_id from assetlife left join StopCode as s on assetlife.assetStopCode_id=s.id where  (assetOfflineFrom between '{0}' and '{1}') and assetSetOfflineByUser_id={2} group by assetStopCode_id".format(start,end,userid))
        return AssetLife.objects.raw("select sum(timestampdiff(MINute,cast(concat(assetOfflineFrom, ' ', assetOfflineFromTime) as datetime),cast(concat(assetOnlineFrom, ' ',assetOnlineFromTime) as datetime))) as id,s.stopDescription as d2,assetStopCode_id from assetlife left join StopCode as s on assetlife.assetStopCode_id=s.id where  (assetOfflineFrom between '{0}' and '{1}') and assetLifeAssetid_id={2} group by assetStopCode_id".format(start,end,assetid))
    #########################################################################################
    @staticmethod
    def GetDowntimeHitsReasonByAsset(start,end,assetid):
        # print("select count(assetlife.id) as id,s.stopDescription as d2,assetStopCode_id from assetlife left join StopCode as s on assetlife.assetStopCode_id=s.id where  (assetOfflineFrom between '{0}' and '{1}') and assetSetOfflineByUser_id={2} group by assetStopCode_id".format(start,end,userid))
        return AssetLife.objects.raw("""select count(assetlife.id) as id,s.causeDescription as d2,s.id from assetlife
         join workorder as wo on wo.id=assetlife.assetWOAssoc_id
         left join CauseCode as s on wo.woCauseCode_id=s.id where  (assetOfflineFrom between '{0}' and '{1}') and assetLifeAssetid_id={2} group by s.id""".format(start,end,assetid))
    #########################################################################################
    @staticmethod
    def GetAssetWoByMType(start,end,assetid):

        return WorkOrder.objects.raw(""" select count(wo.id) as id,maintenanceType_id,m.name as name from workorder as wo
        inner join maintenancetype as m on wo.maintenanceType_id=m.id
        where (wo.datecreated between '{0}' and '{1}') and wo.woAsset_id={2} and isScheduling=0 and visibile=1
        group by maintenanceType_id

         """.format(start,end,assetid))

    @staticmethod
    def clone_asset(id):
            foo=Asset.objects.get(pk=id)
            foo.assetName=foo.assetName+' copy'
            foo.pk=None
            foo.save()
            #############
            foo_part=AssetPart.objects.filter(assetPartAssetid=id)
            for i in foo_part:
                i.pk=None
                i.assetPartAssetid=foo
                i.save()
            #############
            foo_bom=BOMGroupAsset.objects.filter(BOMGroupAssetAsset=id)
            for i in foo_bom:
                i.pk=None
                i.BOMGroupAssetAsset=foo
                i.save()
            ####################
            ###meter reading must not be copied,Because it is unique for it's asset
            foo_files=AssetFile.objects.filter(assetFileAssetId=id)
            for foo_file in foo_files:
                foo_file.pk=None
                foo_file.assetFileAssetId=foo

                foo_file.save()
    # @staticmethod
    # def find_temp_assetcode(foo,pishvand):
    #     max_digit=Asset.objects.filter(assetCode__contains="{}-{}-{}".format(foo.get_asset_loc_code(),foo.assetCategory.code,pishvand)).count()
    #     return "{}-{}-{}{}".format(foo.get_asset_loc_code(),foo.assetCategory.code,pishvand,max_digit+1)
    @staticmethod
    def find_suggested_assetcode(foo,pishvand):
        max_digit=Asset.objects.filter(assetCode__contains="{}-{}-{}".format(foo.get_asset_loc_code(),foo.assetCategory.code,pishvand)).count()
        return "{}-{}-{}{}".format(foo.get_asset_loc_code(),foo.assetCategory.code,pishvand,max_digit+1)
    @staticmethod
    def duplicate_asset(id,tedad,pishvand):
            foo=Asset.objects.get(pk=id)
            foo.pk=None
            foo.assetName=foo.assetName+' '+str(tedad)
            # foo.assetCode=pishvand+' '+str(tedad)
            foo.assetCode=AssetUtility.find_temp_assetcode(foo,pishvand)
            # این دو خط رو نسبت به clone اضافه تر داره
            foo.assetIsLocatedAt=None
            foo.assetIsPartOf=None
            foo.assetStatus=True
            foo.save()
            #############
            foo_bom=BOMGroupAsset.objects.filter(BOMGroupAssetAsset=id)
            for i in foo_bom:
                i.pk=None
                i.BOMGroupAssetAsset=foo
                i.save()

            ############
            foo_part=AssetPart.objects.filter(assetPartAssetid=id)
            for i in foo_part:
                i.pk=None
                i.assetPartAssetid=foo
                i.save()
            ####################
            ###meter reading must not be copied,Because it is unique for it's asset
            foo_files=AssetFile.objects.filter(assetFileAssetId=id)
            for foo_file in foo_files:
                foo_file.pk=None
                foo_file.assetFileAssetId=foo

                foo_file.save()
    @staticmethod
    def getAssets(searchStr):
        result=Asset.objects.all()
        q=searchStr
        for qstr in q:
                 if(qstr.isdigit()):
                     result = result.filter(Q(assetName__icontains=qstr)|Q(assetCode__icontains=qstr)|Q(id=int(qstr))|Q(assetCategory__name__icontains=qstr)).order_by('-id')
                 else:
                    result= result.filter(Q(assetName__icontains=qstr)|Q(assetCode__icontains=qstr)
                                       |Q(assetCategory__name__icontains=qstr)).order_by('-id')
        # (Q(assetName__icontains=qstr)|Q(assetCode__icontains=qstr)|Q(assetCategory__name__icontains=qstr))).order_by('-id')
        result=result.extra(select={'length':'Length(assetName)'}).order_by('length').values('id', 'assetName','assetCode')[:10]
        return result
    # res= Asset.objects.filter(assetName__isnull=False).filter(Q(assetName__icontains=searchStr)|Q(assetCode__icontains=searchStr)).values('id', 'assetName','assetCode')[:10]
    #     return res
    @staticmethod
    def fin_max_pishvand(pishvand):
        return 10
