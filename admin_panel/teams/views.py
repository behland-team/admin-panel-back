from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import TeamMember
from .serializers import TeamMemberSerializer

class TeamMemberViewSet(ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer

