from rest_framework import serializers
from cmms.models import WorkOrder,SysUser,Asset,testuser,MaintenanceType

class MaintenanceTypeSerializer(serializers.ModelSerializer):


    class Meta:
        model = MaintenanceType
        fields = ('id', 'color','name')

class WOSerializer(serializers.ModelSerializer):
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


    class Meta:
        model = WorkOrder
        fields = ('id', 'summaryofIssue', 'datecreated', 'RequestedUser', 'maintenanceType','woAsset','assignedToUser','woStatus','workInstructions','timecreated','woPriority')
class userSerializer(serializers.ModelSerializer):


    class Meta:
        model = testuser
        fields = ('id', 'massage')
