# leads/api_views.py
from rest_framework import viewsets, permissions
from .models import TeamMember
from .serializers import CRESerializer

class CREViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.all().order_by("name")
    serializer_class = CRESerializer
    permission_classes = [permissions.IsAuthenticated]  # or as you prefer
