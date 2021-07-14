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

from cmms.models.parts import *
#from django.core import serializers
import json
from django.forms.models import model_to_dict

from django.urls import reverse_lazy
from django.db import transaction



def list_purchaseboard(request,id=None):
    #
    books = Part.objects.all()
    return render(request, 'cmms/purchase_board/purchaseBoardList.html', {'rfq': books})


##########################################################
