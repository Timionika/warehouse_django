from rest_framework import serializers
from rest_framework import validators

from api.models import ApiUser, Warehouse, Good, Inventory


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128, validators=[
        validators.UniqueValidator(ApiUser.objects.all())
    ])
    email = serializers.EmailField(validators=[
        validators.UniqueValidator(ApiUser.objects.all())
    ])
    password = serializers.CharField(min_length=6, max_length=20, write_only=True)

    user_type = serializers.ChoiceField(
        choices=[
            ('provider', 'Поставщик'),
            ('consumer', 'Потребитель'),
        ]
    )


    def update(self, instance, validated_data):
        if email := validated_data.get("email"):
            instance.email = email
            instance.save(update_fields=["email"])

        if password := validated_data.get("password"):
            instance.set_password(password)
            instance.save(update_fields=["password"])
        return instance

    def create(self, validated_data):
        user = ApiUser.objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
            user_type=validated_data["user_type"]
        )

        user.set_password(validated_data["password"])
        user.save(update_fields=["password"])
        return user



class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}


class GoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Good
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}

class SupplySerializer(serializers.Serializer):
    warehouse = WarehouseSerializer()
    good = GoodSerializer()
    quantity = serializers.IntegerField(min_value=1)

    def to_internal_value(self, data):
        warehouse_data = data.get('warehouse')
        good_data = data.get('good')

        # Поддержка нескольких форматов:
        warehouse_id = None
        if isinstance(warehouse_data, dict):
            warehouse_id = warehouse_data.get('id')
        if isinstance(warehouse_data, (int, str)):
            warehouse_id = warehouse_data
        else:
            raise serializers.ValidationError({'warehouse': 'Неверный формат данных'})

        good_id = None
        if isinstance(good_data, dict):
            good_id = good_data.get('id')
        elif isinstance(good_data, (int, str)):
            good_id = good_data
        else:
            raise serializers.ValidationError({'good': 'Неверный формат данных'})

        try:
            warehouse = Warehouse.objects.get(id=warehouse_id)
        except Warehouse.DoesNotExist:
            raise serializers.ValidationError({'warehouse': 'Склад с таким ID не существует'})

        try:
            good = Good.objects.get(id=good_id)
        except Good.DoesNotExist:
            raise serializers.ValidationError({'good': 'Товар с таким ID не существует'})

        try:
            quantity = int(data.get('quantity'))
        except:
            raise serializers.ValidationError({'quantity': 'Количество должно быть положительным целым числом'})

        return {
        'warehouse': warehouse,
        'good': good,
        'quantity': quantity
        }
    
    def create(self, validated_data):
        warehouse = validated_data['warehouse']
        good = validated_data['good']
        quantity = validated_data['quantity']

        inventory, created = Inventory.objects.get_or_create(
            warehouse=warehouse,
            good=good,
            defaults={'quantity': quantity}
        )

        if not created:
            inventory.quantity += quantity
            inventory.save()

        return inventory
    

    




class WithdrawSerializer(serializers.Serializer):
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all())
    good = serializers.PrimaryKeyRelatedField(queryset=Good.objects.all())
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        warehouse = data['warehouse']
        good = data['good']
        quantity = data['quantity']

        try:
            inventory = Inventory.objects.get(warehouse=warehouse, good=good)
        except Inventory.DoesNotExist:
            raise serializers.ValidationError({
                'detail': 'Товар отсутствует на этом складе'
            })

        if inventory.quantity < quantity:
            raise serializers.ValidationError({
                'quantity': f'Недостаточно товара. Доступно: {inventory.quantity} шт.'
            })

        data['inventory'] = inventory
        return data

    def create(self, validated_data):
        inventory = validated_data['inventory']
        quantity = validated_data['quantity']

        inventory.quantity -= quantity
        inventory.save()
        return inventory
