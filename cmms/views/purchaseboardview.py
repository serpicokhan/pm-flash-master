'''
 fmt = getattr(settings, 'LOG_FORMAT', None)
 lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

 logging.basicConfig(format=fmt, level=lvl)
 logging.debug(nebusinessbject.OrderId.id)
 '''
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Sum
import jdatetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators import csrf
import django.core.serializers
import logging
from django.conf import settings

from cmms.models.stock import *
#from django.core import serializers
import json
from django.forms.models import model_to_dict

from django.urls import reverse_lazy
from django.db import transaction

from cmms.business.PartUtility import *
from django.db.models import F

def list_purchaseboard(request,id=None):
    #
    # books = Part.objects.all()
    # wos=PartUtility.doPaging(request,books)
    wos=Stock.objects.filter(qtyOnHand__lt=F('minQty'))
    # wos=Stock.objects.raw("select count(id) as id ,sum(qtyOnHand) as q1 ,sum(minQty) as q2, stockItem_id from stocks group by stockItem_id,location_id having q1<q2 ")
    return render(request, 'cmms/purchase_board/purchaseBoardList.html', {'rfq': wos})


##########################################################
