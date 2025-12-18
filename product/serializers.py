from rest_framework import serializers

from product.models import Product

CountryChoices = (
        ('TW', 'Taiwan'),
        ('LA', 'Laos'),
        ('NO', 'Norway'),
        ('KG', 'Kyrgyzstan'),
        ('AT', 'Austria'),
        ('CH', 'China'),
    )

class CreateProductSerializer(serializers.Serializer):

    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()
    country = serializers.ChoiceField(choices=CountryChoices)

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError('price can not be negative')
        return price

    def validate(self, attrs):
        quantity = attrs.get('quantity')
        country = attrs.get('country')
        print(country)
        if quantity < 0:
            raise serializers.ValidationError('quantity can not be empty')
        return attrs

    def create(self, validated_data):
        product = Product.objects.create_product(**validated_data)
        return product

class UpdateProductSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    quantity = serializers.IntegerField(required=False)
    country = serializers.ChoiceField(choices=CountryChoices, required=False)

    def validate(self, attrs):
        quantity = attrs.get('quantity')
        price = attrs.get('price')

        if quantity and quantity < 0:
            raise serializers.ValidationError('quantity can not be negative')

        if price and price < 0:
            raise serializers.ValidationError('price can not be negative')

        return attrs

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.country = validated_data.get('country', instance.country)
        instance.save()
        return instance