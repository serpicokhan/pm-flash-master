from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <-- Here
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators import csrf
import django.core.serializers
import logging
from django.conf import settings
from django.contrib.admin.models import LogEntry, ADDITION,CHANGE,DELETION
from django.contrib.contenttypes.models import ContentType
from cmms.models.workorder import *
from cmms.api.WOSerializer import *
from cmms.business.WOUtility import WOUtility


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # print(request.user)


        content = {'message': 'Hello, World!'}
        return Response(content)

class MiniView(APIView):
    def filterUser(self,request,books):
        if(request.user.username!="admin" and  not request.user.groups.filter(name='operator').exists()):
            books = books.filter(Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))).order_by('-datecreated','-timecreated')
        else:
            books=books.order_by('-datecreated','-timecreated')
        return books
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        # print("!23")
        posts = WorkOrder.objects.filter(isScheduling=False,summaryofIssue__isnull=False,visibile=True).order_by('-datecreated')
        companies=self.filterUser(request,posts)
        wos=WOUtility.doPaging(request,companies)
        serializer = WOSerializer(wos, many=True)
        # for k in serializer.data:
        #     # k.datecreated=DateJob.getDate2(k.datecreated)
        #     k["datecreated"]= str(jdatetime.datetime.fromgregorian(date=datetime.datetime.strptime(k["datecreated"], "%Y-%m-%d").date()).date()).replace('-','/')
        return Response(serializer.data)
class RegMiniView(APIView):
    def filterUser(self,request,books):
        if(request.user.username!="admin" and  not request.user.groups.filter(name='operator').exists()):
            books = books.filter(Q(assignedToUser__userId=request.user)|Q(id__in=WorkorderUserNotification.objects.filter(woNotifUser__userId=request.user).values_list('woNotifWorkorder'))).order_by('-datecreated','-timecreated')
        else:
            books=books.order_by('-datecreated','-timecreated')
        return books
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        # print("!23")
        serializer = MiniWorkorderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            posts = WorkOrder.objects.filter(isScheduling=False,summaryofIssue__isnull=False,visibile=True).order_by('-datecreated')
            companies=self.filterUser(request,posts)
            wos=WOUtility.doPaging(request,companies)
            serializer = WOSerializer(wos, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
