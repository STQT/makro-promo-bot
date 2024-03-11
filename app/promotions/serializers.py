from rest_framework import serializers

from app.promotions.models import PromotionCode
from app.users.models import TelegramUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = TelegramUser


class PromotionCodeSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        fields = "__all__"
        model = PromotionCode
