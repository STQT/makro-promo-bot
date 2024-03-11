from rest_framework.generics import RetrieveAPIView

from app.promotions.models import PromotionCode
from app.promotions.serializers import PromotionCodeSerializer


class CodeAPIView(RetrieveAPIView):
    queryset = PromotionCode.objects.select_related("user")
    serializer_class = PromotionCodeSerializer
    lookup_field = 'code'
