from rest_framework.routers import DefaultRouter

from api.views import UserModelViewSet, WarehouseModelViewSet, GoodModelViewSet, InventoryModelViewSet

router = DefaultRouter()

router.register('user', UserModelViewSet)
router.register('warehouses', WarehouseModelViewSet)
router.register('goods', GoodModelViewSet)
router.register('inventory', InventoryModelViewSet)




urlpatterns = [

]

urlpatterns.extend(router.urls)
