from cmms.models.workorder import *
from cmms.business.DateJob import *

class MTTR:
    @staticmethod
    def getMtbfAll(start,end):

                    return AssetLife.objects.raw(''' select a.id as id,a.assetname as name,
                    a.assetcode as code,getdownhits(a.id,'{0}','{1}') as downhits,mtbf(a.id,'{0}','{1}') as mtf
                    from assets a '''.format(start,end))
    @staticmethod
    def GetCurrentMonthMTTR():
        return WorkOrder.objects.raw("SELECT woStatus,dateCompleted, format(sum(TIMESTAMPDIFF(SECOND,datecompleted,datecreated)/3600),2)/count(id) as id from workorder where woStatus=8 and pmonth(datecompleted)=pmonth(current_date) group by woStatus,dateCompleted");
    @staticmethod
    def GetLastMonthMTTR():
        return WorkOrder.objects.raw("SELECT woStatus,dateCompleted, format(sum(TIMESTAMPDIFF(SECOND,datecompleted,datecreated)/3600),2)/count(id) as id from workorder where woStatus=8 and pmonth(datecompleted)=pmonth(CURRENT_DATE - INTERVAL 1 MONTH) group by woStatus,dateCompleted");
    ###########################
    @staticmethod
    def getMTTR(start,end):
        #return WorkOrder.objects.raw("SELECT woStatus,dateCompleted, format(sum(TIMESTAMPDIFF(SECOND,concat(datecompleted,' ',timecompleted),concat(datecreated,' ',timecreated))/3600),0) as id from workorder where woStatus=7 and (datecompleted between '{0}' and '{1}') group by woStatus,dateCompleted".format(start,end));
        return WorkOrder.objects.raw("SELECT format(avg(actualLabor),0) as id from workorder where woStatus=7 and (datecompleted between '{0}' and '{1}')".format(start,end));
    @staticmethod
    def getMTTRAll(start,end,location=None,category=None):
                    where_str=''
                    where_loc=""

                    if(category):
                        where_str+='and t4.assetCategory_id in ({0})'.format( ",". join(category) )
                    if(location):
                        where_str+='and (t4.assetIsLocatedAt_id in ({0})) or t4.id in ({0})'.format( ",". join(location) )


                    # return AssetLife.objects.raw(''' select a.id as id,a.assetname as name,a.assetcode as code
                    #                              ,getdownhits(a.id,'{0}','{1}') as downhits,
                    #                              mttr(a.id,'{0}','{1}') as mtt
                    # from assets a
                    #
                    # order by downhits desc
                    #
                    #
                    #
                    #                '''.format(start,end))
                    #

                    return Tasks.objects.raw(""" select (t31/t32) as id,dt1 from
                    (select (sum(timestampdiff(MINute,cast(concat(t1.taskStartDate, ' ', t1.taskStartTime) as datetime)
                    ,cast(concat(t1.taskDateCompleted, ' ',t1.taskTimeCompleted) as datetime))))/60 as t31,taskStartDate as dt1,t3.id
                     from tasks as t1 left join workorder as t3 on t1.workorder_id=t3.id
                     left join assets t4 on t4.id=t3.woAsset_id
                      where t3.isScheduling=0 and t3.visibile=1 and t3.maintenancetype_id=18 and t1.taskStartDate between '{0}' and '{1}'
                      {2}
                        group by dt1 having t31 is not null) as a left join
                       (select COALESCE(count(t1.id),0) as t32,t1.taskstartdate dt2 ,workorder.id
                       from tasks t1 left join workorder on t1.workorder_id=workorder.id
                       left join assets t4 on t4.id=workorder.woAsset_id
                        where workorder.maintenanceType_id=18
                        and isScheduling=0 and visibile=1 and t1.taskStartDate between '{0}' and '{1}'
                        {2}
                         group by t1.taskstartdate )
                         as b on a.dt1=b.dt2; """.format(start,end,where_str))
    @staticmethod
    def getMTTRAll2(start,end,location=None,category=None):
                    where_str=''
                    where_str1=''
                    where_loc=""

                    if(category):
                        where_str+='and t4.assetCategory_id in ({0})'.format( ",". join(category) )
                    if(location):
                        if(location!='-1' ):
                            print("location",location)
                            where_str+='and (t3.woAsset_id in (select id from assets where id={0} or assetIsLocatedAt_id={0}))'.format( location )
                            where_str1+='and (workorder.woAsset_id in (select id from assets where id={0} or assetIsLocatedAt_id={0}))'.format( location )


                    # return AssetLife.objects.raw(''' select a.id as id,a.assetname as name,a.assetcode as code
                    #                              ,getdownhits(a.id,'{0}','{1}') as downhits,
                    #                              mttr(a.id,'{0}','{1}') as mtt
                    # from assets a
                    #
                    # order by downhits desc
                    #
                    #
                    #
                    #                '''.format(start,end))
                    #

                    return Tasks.objects.raw(""" select (t31/t32) as id,dt1 from
                    (select (sum(timestampdiff(MINute,cast(concat(t1.taskStartDate, ' ', t1.taskStartTime) as datetime)
                    ,cast(concat(t1.taskDateCompleted, ' ',t1.taskTimeCompleted) as datetime))))/60 as t31,taskStartDate as dt1,t3.id
                     from tasks as t1 left join workorder as t3 on t1.workorder_id=t3.id
                     left join assets t4 on t4.id=t3.woAsset_id
                      where t3.isScheduling=0 and t3.visibile=1 and t3.maintenancetype_id=18 and t1.taskStartDate between '{0}' and '{1}'
                      {2}
                        group by dt1 having t31 is not null) as a left join
                       (select COALESCE(count(t1.id),0) as t32,t1.taskstartdate dt2 ,workorder.id
                       from tasks t1 left join workorder on t1.workorder_id=workorder.id
                       left join assets t4 on t4.id=workorder.woAsset_id
                        where workorder.maintenanceType_id=18
                        and isScheduling=0 and visibile=1 and t1.taskStartDate between '{0}' and '{1}'
                        {3}
                         group by t1.taskstartdate )
                         as b on a.dt1=b.dt2; """.format(start,end,where_str,where_str1))

    @staticmethod
    def getMTTRByCategory(category,start,end):
        wherestr="where 1=1 "

        if(category):
            # print(category,"###############")
            wherestr+=" and c.id={0}".format(category)
            #using left join to cover empty isPartOf
        return AssetLife.objects.raw(''' select a.id as id,
                    a.assetname as name,a.assetcode as code,
                    getdownhits(a.id,'{0}','{1}') as downhits,
                    mttr(a.id,'{0}','{1}') as mtt
                    from assets a
                    left join assetcategory c on a.assetcategory_id=c.id
                    {2}
                    order by downhits desc




                                   '''.format(start,end,wherestr))


    @staticmethod
    def getMTBFByCategory(category,start,end):
        wherestr="where 1=1 "

        if(category):
            # print(category,"###############")
            wherestr+=" and c.id={0}".format(category)
        #using left join to cover empty isPartOf
        return AssetLife.objects.raw(''' select a.id as id,
                    a.assetname as name,a.assetcode as code,

                    getdownhits(a.id,'{0}','{1}') as downhits,
                    mtbf(a.id,'{0}','{1}') as mtf
                    from assets a

                    left join assetcategory c on a.assetcategory_id=c.id
                    {2} {3}


                                   '''.format(start,end,wherestr,'order by mtf'))

    @staticmethod
    def getTotalMTTR(id):
        return AssetLife.objects.raw('select total_mttr({0}) as id'.format(id))
    @staticmethod
    def getTotalMTBF(id):
        return AssetLife.objects.raw('select total_mtbf({0}) as id'.format(id))
    # @staticmethod
    # def get_mtbf_asset_period(assetID,priod,dt1):
    #     #priod:1 =>1 mahe 2=>3 mahe
    #     if(priod==1):
    #         return MTTR.get_mtbf_asset_mahane(assetID,dt1)
    #     # else:
    #     #     return MTTR.get_mtbf_asset_3mahe(assetID,dt1)
    #     return None
    @staticmethod
    def get_mtbf_asset_mahane(assetID,dt1):
        mtbf_vector={}
        for i in utilMDate:
            dt_start=dt1 + '-' + utilMDate[i][0] #eg 1400-01-01
            dt_end=dt1 + '-' + utilMDate[i][1] #eg 1400-01-31
            mtbf_vector[i]=MTTR.get_mtbf_date_asset(assetID,DateJob.getDate2(dt_start),DateJob.getDate2(dt_end))
        return mtbf_vector
    @staticmethod
    def get_mtbf_date_asset(assetID,start,end):
        # print("select mtbf({0},'{1}','{2}') as id".format(assetID,start,end))
        if(end > datetime.datetime.now().date()):
            return 0
        return AssetLife.objects.raw("select mtbf({0},'{1}','{2}') as id".format(assetID,start,end))[0].id
    @staticmethod
    def get_mtbf_asset_mahane_by_cause(assetID,dt1,causecode):
        mtbf_vector={}
        for i in utilMDate:
            dt_start=dt1 + '-' + utilMDate[i][0] #eg 1400-01-01
            dt_end=dt1 + '-' + utilMDate[i][1] #eg 1400-01-31
            mtbf_vector[i]=MTTR.get_mtbf_date_asset_cause(assetID,DateJob.getDate2(dt_start),DateJob.getDate2(dt_end),causecode)
        return mtbf_vector
    @staticmethod
    def get_mtbf_date_asset_cause(assetID,start,end,cid):
        # print("select mtbf({0},'{1}','{2}') as id".format(assetID,start,end))
        if(end > datetime.datetime.now().date()):
            return 0
        return AssetLife.objects.raw("select mtbfbycausecode({0},{1},'{2}','{3}') as id".format(assetID,cid,start,end))[0].id
