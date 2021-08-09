from rest_framework import serializers
from cmms.models import WorkOrder,SysUser,Asset,testuser,MaintenanceType
import jdatetime
import datetime

class MaintenanceTypeSerializer(serializers.ModelSerializer):


    class Meta:
        model = MaintenanceType
        fields = ('id', 'color','name')

class WOSerializer(serializers.ModelSerializer):
    datecreated = serializers.SerializerMethodField()
    RequestedUser = serializers.SlugRelatedField(
        queryset=SysUser.objects.all(), slug_field='fullName'
    )
    assignedToUser = serializers.SlugRelatedField(
        queryset=SysUser.objects.all(), slug_field='fullName'
    )
    woAsset = serializers.SlugRelatedField(
        queryset=Asset.objects.all(), slug_field='assetName'
    )
    maintenanceType =MaintenanceTypeSerializer(read_only=True)
    def get_datecreated(self, obj):
         return  str(jdatetime.datetime.fromgregorian(date=obj.datecreated).date())
    #  serializers.SlugRelatedField(
    #     queryset=MaintenanceType.objects.all(), slug_field='id'
    # )
    # color = serializers.SlugRelatedField(
    #     queryset=MaintenanceType.objects.all(), slug_field='color'
    # )


    class Meta:
        model = WorkOrder
        fields = ('id', 'summaryofIssue', 'datecreated', 'RequestedUser', 'maintenanceType','woAsset','assignedToUser',
        'woStatus','workInstructions','timecreated')
class WOSerializerDetaile(serializers.ModelSerializer):
    datecreated = serializers.SerializerMethodField()
    RequestedUser = serializers.SlugRelatedField(
        queryset=SysUser.objects.all(), slug_field='fullName'
    )
    assignedToUser = serializers.SlugRelatedField(
        queryset=SysUser.objects.all(), slug_field='fullName'
    )
    woAsset = serializers.SlugRelatedField(
        queryset=Asset.objects.all(), slug_field='assetName'
    )
    maintenanceType =MaintenanceTypeSerializer(read_only=True)
    # maintenanceType = serializers.SlugRelatedField(
    #     queryset=MaintenanceType.objects.all(), slug_field='id'
    # )
    def get_datecreated(self, obj):
         return  str(jdatetime.datetime.fromgregorian(date=obj.datecreated).date())


    class Meta:
        model = WorkOrder
        fields = ('id', 'summaryofIssue', 'datecreated', 'RequestedUser', 'maintenanceType','woAsset','assignedToUser','woStatus','workInstructions','timecreated','woPriority')
class userSerializer(serializers.ModelSerializer):


    class Meta:
        model = testuser
        fields = ('id', 'massage')
