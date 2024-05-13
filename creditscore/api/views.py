from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from creditscore.models import UserProfile
from .serializers import ProfileSerializer

@api_view(['GET'])
def getroutes(request):
    routes = [
        
        'GET /api/profile/'
        'GET /api/creditscore'

    ]
    return Response(routes)

@api_view(['GET'])
def getProfiles(request):
    Profile= UserProfile.objects.all()
    serializer=ProfileSerializer(Profile, many=True)
    return Response(serializer.data) 

    