from cmms.models import RingAmar

from cmms.business.systemmessage import *
from django.core.paginator import *
from django.db.models import Sum


class AmarUtility:

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
    def getTolid(start,end,location=None):

        values=RingAmar.objects.raw('''SELECT `ringamar`.`assetAmarDate`,
                                    SUM(`ringamar`.`assetTotlaKilometer`) AS `id` FROM `ringamar`
                                    INNER JOIN `assets` ON (`ringamar`.`assetName_id` = `assets`.`id`)
                                     WHERE (`ringamar`.`assetAmarDate` BETWEEN '{0}' AND '{1}' AND
                                     `assets`.`assetIsLocatedAt_id` = {2}) GROUP BY `ringamar`.`assetAmarDate`'''.format(start,end,location))
        values2=RingAmar.objects.raw('''SELECT `ringamar`.`assetAmarDate` ,`ringamar`.`shifttypes`,SUM(`ringamar`.`assetTotlaKilometer`) AS `id`  FROM `ringamar`
                                    INNER JOIN `assets` ON (`ringamar`.`assetName_id` = `assets`.`id`)
                                     WHERE (`ringamar`.`assetAmarDate` BETWEEN '{0}' AND '{1}' AND
                                     `assets`.`assetIsLocatedAt_id` = {2}) GROUP BY `ringamar`.`assetAmarDate`,`ringamar`.`shifttypes`'''.format(start,end,location))
        return (values,values2)
    @staticmethod
    def getTolidMain(start,end,location=None):

        values=RingAmar.objects.raw('''SELECT `tolidamar`.`registered_date`,
                                    SUM(`tolidamar`.`meghdar`) AS `id` FROM `tolidamar`
                                    INNER JOIN `assets` ON (`tolidamar`.`location_id` = `assets`.`id`)
                                     WHERE (`tolidamar`.`registered_date` BETWEEN '{0}' AND '{1}' AND
                                     `assets`.`id` = {2}) GROUP BY `tolidamar`.`registered_date`'''.format(start,end,location))
        # values2=RingAmar.objects.raw('''SELECT `TolidAmar`.`assetAmarDate` ,`TolidAmar`.`shifttypes`,SUM(`TolidAmar`.`assetTotlaKilometer`) AS `id`  FROM `TolidAmar`
        #                             INNER JOIN `assets` ON (`TolidAmar`.`assetName_id` = `assets`.`id`)
        #                              WHERE (`TolidAmar`.`assetAmarDate` BETWEEN '{0}' AND '{1}' AND
        #                              `assets`.`assetIsLocatedAt_id` = {2}) GROUP BY `TolidAmar`.`assetAmarDate`,`ringamar`.`shifttypes`'''.format(start,end,location))
        # return (values,values2)
        return values
    @staticmethod
    def getTolidBar(start,end,location=None):
        print('''SELECT (pyear(assetamardate)) AS jalali_year,
                           (pmonth(assetamardate)) AS jalali_month,
                           SUM(a.assetTotlaKilometer) AS sum_value,b.assetIsLocatedAt_id as id
                            FROM ringamar as a
                            left join  assets as b on a.assetName_id=b.id
                            where b.assetIsLocatedAt_id={0}
                            GROUP BY jalali_year, jalali_month,b.assetIsLocatedAt_id'''.format(location))

        values=RingAmar.objects.raw('''SELECT (pyear(assetamardate)) AS jalali_year,
                           (pmonth(assetamardate)) AS jalali_month,
                           SUM(a.assetTotlaKilometer) AS sum_value,b.assetIsLocatedAt_id as id
                            FROM ringamar as a
                            left join  assets as b on a.assetName_id=b.id
                            where b.assetIsLocatedAt_id={0}
                            GROUP BY jalali_year, jalali_month,b.assetIsLocatedAt_id'''.format(location))
        return values
    @staticmethod
    def getTolidBarAPI(location=None):

        values=RingAmar.objects.raw('''SELECT `ringamar`.`assetAmarDate`,
                                    SUM(`ringamar`.`assetTotlaKilometer`) AS `id` FROM `ringamar`
                                    INNER JOIN `assets` ON (`ringamar`.`assetName_id` = `assets`.`id`)
                                     WHERE(
                                     `assets`.`assetIsLocatedAt_id` = {0})  GROUP BY `ringamar`.`assetAmarDate` order by `ringamar`.`assetAmarDate`'''.format(location))[1:30]
        # values=RingAmar.objects.raw('''SELECT YEAR(pdate(assetamardate)) AS jalali_year,
        #                    MONTH(pdate(assetamardate)) AS jalali_month,
        #                    SUM(a.assetTotlaKilometer) AS sum_value,b.assetIsLocatedAt_id as id,a.shifttypes
        #                     FROM ringamar as a
        #                     left join  assets as b on a.assetName_id=b.id
        #                     where b.assetIsLocatedAt_id={0}
        #                     GROUP BY jalali_year, jalali_month,b.assetIsLocatedAt_id,a.shifttypes'''.format(location))
        return values
    @staticmethod
    def getTolidByShift(start,end,location=None):
        values2=RingAmar.objects.raw('''SELECT `ringamar`.`assetAmarDate` ,`ringamar`.`shifttypes`,SUM(`ringamar`.`assetTotlaKilometer`) AS `id`  FROM `ringamar`
                                    INNER JOIN `assets` ON (`ringamar`.`assetName_id` = `assets`.`id`)
                                     WHERE (`ringamar`.`assetAmarDate` BETWEEN '{0}' AND '{1}' AND
                                     `assets`.`assetIsLocatedAt_id` = {2}) GROUP BY `ringamar`.`assetAmarDate`,`ringamar`.`shifttypes`'''.format(start,end,location))
        return values2
    @staticmethod
    def getTolidTime(start,end,location=None):
        values=RingAmar.objects.raw('''SELECT `ringamar`.`assetAmarDate`,
                                    SUM(`ringamar`.`assetTotalTime`) AS `id` FROM `ringamar`
                                    INNER JOIN `assets` ON (`ringamar`.`assetName_id` = `assets`.`id`)
                                     WHERE (`ringamar`.`assetAmarDate` BETWEEN '{0}' AND '{1}' AND
                                     `assets`.`assetIsLocatedAt_id` = {2}) GROUP BY `ringamar`.`assetAmarDate`'''.format(start,end,location))
        values2=RingAmar.objects.raw('''SELECT `ringamar`.`assetAmarDate`,`ringamar`.`shifttypes`,
                                    SUM(`ringamar`.`assetTotalTime`) AS `id` FROM `ringamar`
                                    INNER JOIN `assets` ON (`ringamar`.`assetName_id` = `assets`.`id`)
                                     WHERE (`ringamar`.`assetAmarDate` BETWEEN '{0}' AND '{1}' AND
                                     `assets`.`assetIsLocatedAt_id` = {2}) GROUP BY `ringamar`.`assetAmarDate`,`ringamar`.`shifttypes`'''.format(start,end,location))
        return (values,values2)
