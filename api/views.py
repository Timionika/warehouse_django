from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.models import ApiUser, Warehouse, Good, Inventory
from api.serializers import UserSerializer, WarehouseSerializer, GoodSerializer, InventorySerializer, SupplySerializer, WithdrawSerializer
from api.permissions import IsConsumer, IsProvider, IsSuperuser

class UserModelViewSet(viewsets.ModelViewSet):
    queryset = ApiUser.objects.all()
    http_method_names = ['post', 'get']
    serializer_class = UserSerializer

    authentication_classes = []
    permission_classes = []


class WarehouseModelViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

    @action(detail=True)
    def goods(self, request, pk=None):
        wh = get_object_or_404(Warehouse.objects.all(), id=pk)
        available_goods = wh.goods.filter(quantity__gt = 0)
        return Response(
            InventorySerializer(available_goods, many=True).data
        )


class GoodModelViewSet(viewsets.ModelViewSet):
    queryset = Good.objects.all()
    serializer_class = GoodSerializer

    @action(detail=True)
    def warehouses(self, request, pk=None):
        good = get_object_or_404(Good.objects.all(), id=pk)
        available_at_warehouses = good.warehouses.filter(quantity__gt=0)
        return Response(
            InventorySerializer(available_at_warehouses, many=True).data
        )


class InventoryModelViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def create(self, request, *args, **kwargs):
        # Запрещаем POST-запросы на создание инвентаря
        return Response(
            {"detail": "Метод POST не разрешен."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=False, methods=['post'], permission_classes=[IsProvider])
    def supply(self, request):
        serializer = SupplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "ok"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsConsumer])
    def withdraw(self, request):
        serializer = WithdrawSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "ok"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



