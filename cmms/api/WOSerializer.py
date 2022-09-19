from rest_framework import serializers
from cmms.models import WorkOrder,SysUser,Asset,testuser,MaintenanceType,Tasks,Part,WorkorderPart,Stock,WorkorderFile,Asset,AssetCategory,AssetPart,AssetFile,AssetMeterReading,MeterCode

import jdatetime
import datetime

class MaintenanceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceType
        fields = ('id', 'color','name')
class MeterCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeterCode
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysUser
        fields = '__all__'

class AssetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetCategory
        fields = '__all__'
class AssetPartSerializer(serializers.ModelSerializer):
    assetPartPid = serializers.SlugRelatedField(
        queryset=Part.objects.all(), slug_field='partName'
    )
    assetPartAssetid = serializers.SlugRelatedField(
        queryset=Asset.objects.all(), slug_field='assetName'
    )
    class Meta:
        model = AssetPart
        fields = '__all__'
class SubAssetSerializer(serializers.ModelSerializer):
    assetCategory=AssetCategorySerializer(read_only=True)
    class Meta:
        model = Asset
        fields = '__all__'
class AssetMeterReadingSerializer(serializers.ModelSerializer):
    assetMeterMeterReadingUnit=MeterCodeSerializer(read_only=True)

    class Meta:
        model = AssetMeterReading
        fields = '__all__'
class AssetSerializer(serializers.ModelSerializer):
    assetIsPartOf=SubAssetSerializer(read_only=True)
    assetIsLocatedAt=SubAssetSerializer(read_only=True)
    assetCategory=AssetCategorySerializer(read_only=True)


    class Meta:
        model = Asset
        fields = '__all__'


class WorkorderFileSerializer(serializers.ModelSerializer):



    class Meta:
        model = WorkorderFile
        fields = '__all__'
class AssetFileSerializer(serializers.ModelSerializer):



    class Meta:
        model = AssetFile
        fields = '__all__'
class MiniWorkorderSerializer(serializers.ModelSerializer):



    class Meta:
        model = WorkOrder
        fields = ('summaryofIssue','woAsset','maintenanceType','woTags','woStatus')

class TaskSerializer(serializers.ModelSerializer):
    taskAssignedToUser = serializers.SlugRelatedField(
        queryset=SysUser.objects.all(), slug_field='fullName'
    )



    class Meta:
        model = Tasks
        fields = '__all__'
        # exculde=('taskMetrics')
class PartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Part
        fields = '__all__'
class StockSerializer(serializers.ModelSerializer):
    stockItem=PartSerializer(read_only=True)

    class Meta:
        model = Stock
        fields = '__all__'

class woPartSerializer(serializers.ModelSerializer):
    woPartStock =StockSerializer(read_only=True)

    class Meta:
        model = WorkorderPart
        fields = '__all__'


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
