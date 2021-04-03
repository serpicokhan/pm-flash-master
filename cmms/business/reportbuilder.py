from cmms.forms import *
from cmms.models.report import *
from django.shortcuts import get_object_or_404
class ReportBuilder():
    @staticmethod
    def build(repNo):
            r= get_object_or_404(Report, id=int(repNo))
            report=globals()[r.reportClassName]
            return report(),r.reportTemplate
    @staticmethod
    def getReportMethod(repNo):
         r= get_object_or_404(Report, id=int(repNo))
         return r.reportClassName
