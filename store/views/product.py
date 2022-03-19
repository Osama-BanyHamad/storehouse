from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from store.models import Product
from store.serializers import ProductSerializer, ReadProductSerializer
from django.shortcuts import get_object_or_404


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ReadProductSerializer(products, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        request.data["creator"] = request.user.id
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', "PUT", "DELETE"])
def product(request, pk):
    if request.method == 'GET':
        instance = get_object_or_404(Product, pk=pk)
        data = ReadProductSerializer(instance).data

        return Response(data)

    elif request.method == 'DELETE':
        instance = get_object_or_404(Product, pk=pk)
        instance.delete()

        return Response({})

    elif request.method == 'PUT':
        request.data["creator"] = request.user.id
        instance = get_object_or_404(Product, pk=pk)

        serializer = ProductSerializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors)
