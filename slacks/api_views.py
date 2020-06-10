from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@csrf_exempt
@api_view(['POST', ])
def interactive_commands(request):
    print(request.data)
    return Response(status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST', ])
def question(request):
    print(request.data)
    return Response(status=status.HTTP_200_OK)