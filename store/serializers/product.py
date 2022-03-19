from rest_framework import serializers
from store.models import Product, Category
from store.serializers.category import CategorySerializer
from store.serializers.user import UserSerializer


class ProductSerializer(serializers.ModelSerializer):
    categories_ids = serializers.ListField(required=True, write_only=True)
    categories = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        instance = Product()
        categories = validated_data.pop("categories_ids")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        categories_instances = []

        for value in categories:
            category_instance = Category()
            setattr(category_instance, "id", value)
            categories_instances.append(category_instance)

        through = instance.categories.through

        objects = [
            through(product=instance, category=category) for category in categories_instances
        ]

        through.objects.bulk_create(objects)

        return instance

    def update(self, instance, validated_data):

        categories = validated_data.pop("categories_ids")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        categories_instances = []

        for value in categories:
            category_instance = Category()
            setattr(category_instance, "id", value)
            categories_instances.append(category_instance)

        if not self.partial or (self.partial and categories_instances != None):
            through = instance.categories.through
            # queryset = Category.objects.filter(id__in=categories_instances).values_list("id", flat=True)
            objects = [
                through(product=instance, category=category) for category in categories_instances
            ]
            through.objects.filter(category_id=instance.id).delete()

            through.objects.bulk_create(objects)

        return instance


class ReadProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(read_only=True, required=False, many=True)
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class BaseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name"]
