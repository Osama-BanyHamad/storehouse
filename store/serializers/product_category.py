from rest_framework import serializers

from . import CategorySerializer
from ..models import ProductCategories
from store.serializers.product import ReadProductSerializer, BaseProductSerializer


class ProductCategorySerializer(serializers.ModelSerializer):
    product = BaseProductSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = ProductCategories
        fields = ["product", "category"]

