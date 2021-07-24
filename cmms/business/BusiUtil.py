from django.core.paginator import *
from cmms.models.business import *
class BusinessUtility:
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
    @staticmethod
    def seachBusiness(searchStr):

             if(searchStr != 'empty'):
                 return Business.objects.filter(name__contains=searchStr)|Business.objects.filter(code__contains=searchStr)|Business.objects.filter(primaryContact__contains=searchStr)

             else:
                 return Business.objects.all()
