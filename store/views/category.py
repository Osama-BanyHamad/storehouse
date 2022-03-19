from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from store.models import ProductCategories, Product, Category
from store.serializers import ProductCategorySerializer, CategorySerializer
from django.shortcuts import get_object_or_404


@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        """
            Note: The API Logic can be reduced by implementing the group by function, but I used this logic
            to be more clear and readable
        """
        categories = ProductCategories.objects.all()
        serializer = ProductCategorySerializer(categories, many=True)

        set_of_categories = []

        for item in serializer.data:
            if not dict(item["category"]) in set_of_categories:
                set_of_categories.append(dict(item["category"]))

        list_of_categories = []

        for category_object in set_of_categories:
            products = []
            for item in serializer.data:
                if item["category"] == category_object:
                    products.append(item["product"])
            list_of_categories.append({"count": len(products), "category": category_object, "products": products})

        return Response(list_of_categories)

    elif request.method == 'POST':
        request.data["creator"] = request.user.id
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', "PUT", "DELETE"])
def category(request, pk):
    if request.method == 'GET':
        instance = get_object_or_404(Category, pk=pk)
        data = CategorySerializer(instance).data

        return Response(data)

    elif request.method == 'DELETE':
        instance = get_object_or_404(Category, pk=pk)
        instance.delete()

        return Response({})

    elif request.method == 'PUT':
        request.data["creator"] = request.user.id
        instance = get_object_or_404(Category, pk=pk)

        serializer = CategorySerializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors)
