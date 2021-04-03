from django.utils import simplejson
class HandleMyClass(simplejson.JSONEncoder):
     """ simplejson.JSONEncoder extension: handle MyClass"""
     def default(self, obj):
         if isinstance(obj, MyClass):
             return obj.__dict__
         return simplejson.JSONEncoder.default(self, obj)

# data = simplejson.dumps( dictionary, cls=HandleMyClass )
