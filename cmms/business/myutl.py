
class someUtil:
    @staticmethod
    def get_somthoing(id):
        wo=WorkOrder.objects.filter(woAsset__id=self.id,woStatus__in=(1,5,6,9))
        if(wo.count()>0):
            return True
        return False
