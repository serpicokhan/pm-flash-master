from cmms.models.Asset import *
class AssetStatus:
    @staticmethod
    def ReverseAssetStatus(AssetID):
        asset=Asset.objects.get(id=AssetID)
        asset.assetStatus= not asset.assetStatus
        asset.save()
    @staticmethod
    def SetOffline(AssetID):
     asset=Asset.objects.get(id=AssetID)
     asset.assetStatus=False
     asset.save()
    @staticmethod
    def SetOnline(AssetID):
      asset=Asset.objects.get(id=AssetID)
      asset.assetStatus=True
      asset.save()
