from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <-- Here


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print(request.user)


        content = {'message': 'Hello, World!'}
        return Response(content)
