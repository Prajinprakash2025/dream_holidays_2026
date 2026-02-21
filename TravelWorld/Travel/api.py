# leads/api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Lead

SECRET = getattr(settings, "PHP_WEBHOOK_SECRET", "change-me")

class CreateLeadView(APIView):
    def post(self, request):
        # Simple shared-secret check (server-to-server)
        if request.headers.get("X-Webhook-Secret") != SECRET:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data or {}
        lead = Lead.objects.create(
            name=data.get("name",""),
            email=data.get("email"),
            phone=data.get("phone"),
            
        )
        return Response({"id": lead.id, "ok": True}, status=status.HTTP_201_CREATED)
