from cmms.models.workorder import MiscCost
class ExtraCost:
    @staticmethod
    def getCurrentMonthMiscCost():
        return MiscCost.objects.raw("select sum(actualTotlaCoast) as id from misccoast where pmonth(CURRENT_DATE)=pmonth(timeStamp)")
    @staticmethod
    def getLastMonthMiscCost():
          return MiscCost.objects.raw("select sum(actualTotlaCoast) as id from misccoast where pmonth(CURRENT_DATE - INTERVAL 1 month)=pmonth(timeStamp)")

    ###########################
    @staticmethod
    def getMiscCost(start,end):
        # print("!!!!!!!!!!!!!!!!!!!!!")
        # print("select sum(actualTotlaCoast) as id,DATE_FORMAT(FROM_UNIXTIME(`user.registration`), '%e %b %Y') AS 'date_formatted' from misccoast where  date_formatted between '{0}' and '{1}'".format(start,end))
        return MiscCost.objects.raw("select sum(misccoast.qnty*misccoast.actualUnitCoast) as id from misccoast where  date(timestamp) between '{0}' and '{1}'".format(start,end))
    ##############################
    @staticmethod
    def getAvgMiscCost(start,end):
        return MiscCost.objects.raw("SELECT avg(actualTotlaCoast) as id FROM misccoast as t1 INNER JOIN workorder as t2 ON misccoast.miscCoastWorkorder_id = workorder.id where t2.datecreated between '{0}' and '{1}'".format(start,end))
    ###########################################
    #for eq cost
    @staticmethod
    def getMiscCostForAsset(assetId,start,end):
        # print("##############misccost")
        # print("select sum(actualTotlaCoast) as id from misccoast as t1 inner join workorder as t2 on t1.miscCoastWorkorder_id = t2.id where date(t1.timeStamp) between '{0}' and '{1}' and t2.woAsset_id={2}".format(start,end,assetId))
        return MiscCost.objects.raw("select sum(actualTotlaCoast) as id from misccoast as t1 inner join workorder as t2 on t1.miscCoastWorkorder_id = t2.id where date(t1.timeStamp) between '{0}' and '{1}' and t2.woAsset_id={2}".format(start,end,assetId))
