from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializers
from rest_framework import status
# Create your views here.
@api_view(['GET', 'POST'])
def Item_list_view(request, format =None):
    if request.method == 'GET':
        items = Item.objects.all()
        serializer = ItemSerializers(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ItemSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])   
def Item_details_view(request ,pk, format =None):
    try:
        items = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ItemSerializers(items)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ItemSerializers(items, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        items.delete()
        return Response(status=204)
        

