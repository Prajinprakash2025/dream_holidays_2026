from rest_framework import serializers
from .models import *




# app: crm/api.py
from rest_framework import serializers, permissions, views, response, status
from .models import Lead
import os

WEBHOOK_SECRET = os.environ.get("PHP_WEBHOOK_SECRET", "change-me")

# leads/serializers.py (or your file)
from rest_framework import serializers
from .models import Lead

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ["id","name","email","phone","message","from_url","created_at"]
        read_only_fields = ["id","created_at"]

class LeadInSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    message = serializers.CharField(required=False, allow_blank=True)
    from_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class PhpWebhookAuth(permissions.BasePermission):
    """
    Very simple shared-secret header check. Add 'X-Webhook-Secret' from PHP.
    """
    def has_permission(self, request, view):
        return request.headers.get("X-Webhook-Secret") == WEBHOOK_SECRET

class CreateLeadView(views.APIView):
    permission_classes = [PhpWebhookAuth]

    def post(self, request):
        ser = LeadInSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        lead = Lead.objects.create(
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            message=data.get("message"),

        )
        return response.Response(LeadSerializer(lead).data, status=status.HTTP_201_CREATED)


class CRESerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ["id", "name", "email", "phone", "is_active"]

