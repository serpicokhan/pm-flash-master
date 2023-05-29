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
        # values=RingAmar.objects.filter(assetAmarDate__range=(start, end),assetName__assetIsLocatedAt__id=location).values('date').annotate(total_amount=Sum('amount'))
        # values = RingAmar.objects.filter(
        #     assetAmarDate__range=(start, end),assetName__assetIsLocatedAt__id=location
        # ).values('assetAmarDate').annotate(data_sum=Sum('assetTotlaKilometer'))
        # print(RingAmar.objects.filter(
        #     assetAmarDate__range=(start, end),assetName__assetIsLocatedAt__id=location
        # ).values('assetAmarDate').annotate(data_sum=Sum('assetTotlaKilometer')).query)
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
