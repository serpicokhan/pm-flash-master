from django.core.paginator import *
from cmms.models.business import *
from django.db.models import Q
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

             if(searchStr):
                 return Business.objects.filter(name__contains=searchStr)|Business.objects.filter(code__contains=searchStr)|Business.objects.filter(primaryContact__contains=searchStr)

             else:
                 return Business.objects.all()
    @staticmethod
    def getBusiness(searchStr):
            qstr=searchStr
            result=Business.objects.all()

            for q in searchStr:
                result = result.filter(Q(name__contains=qstr)|Q(code__contains=qstr)|Q(primaryContact__contains=qstr)).order_by('-id').values('id', 'name')
            # res= Part.objects.filter(partName__isnull=False).filter(partName__icontains=searchStr)
            result=result.extra(select={'length':'Length(name)'}).order_by('length').values('id', 'name','primaryContact')[:10]

            return result
