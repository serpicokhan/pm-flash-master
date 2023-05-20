from cmms.models import RingAmar

from cmms.business.systemmessage import *
from django.core.paginator import *
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
