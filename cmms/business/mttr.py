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
    def getMTTRAll(start,end):
                    print(''' select a.id as id,a.assetname as name,a.assetcode as code,getdownhits(a.id,'{0}','{1}') as downhits,mttr(a.id,'{0}','{1}') as mtt
                    from assets a     left join assets b on a.id=b.assetisPartOf
                    group by id,name,code,location
                    having downhits>0


                    '''.format(start,end))
                    return AssetLife.objects.raw(''' select a.id as id,a.assetname as name,a.assetcode as code
                                                 ,getdownhits(a.id,'{0}','{1}') as downhits,
                                                 mttr(a.id,'{0}','{1}') as mtt
                    from assets a

                    order by downhits desc



                                   '''.format(start,end))
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
