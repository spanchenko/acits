from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone

from .models import CustomUser, Flat, FlatAttributesValue, RentOrder, FlatRoom, Build


class BuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Build
        fields = '__all__'


class FlatAttributesValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlatAttributesValue
        fields = ('id', 'attribute', 'count')

    def validate(self, attrs):
        if attrs['count'] < 1:
            raise ValidationError(detail="Attributes count should be greater 0")
        return attrs


class FlatRoomSerializer(WritableNestedModelSerializer):
    flat_attributes = FlatAttributesValueSerializer(many=True)
    class Meta:
        model = FlatRoom
        fields = '__all__'
        extra_kwargs = {'flat': {'read_only': True}}
    
    def validate(self, attrs):
        if len(attrs['flat_attributes']) < 2:
            raise ValidationError(detail="You should specify at least two attributes in room")
        return attrs


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        #fields = '__all__'
        exclude = ('password',)


class FlatSerializer(WritableNestedModelSerializer):
    build = BuildSerializer()
    flat_rooms = FlatRoomSerializer(many=True)
    class Meta:
        model = Flat
        fields = '__all__'
        extra_kwargs = {'room_count': {'read_only': True}}
    
    def to_internal_value(self, data):
        data['owner'] = self.context['request'].user.id
        data['build'] = BuildSerializer(Build.objects.get(id=data['build'])).data
        return super().to_internal_value(data)

    def validate(self, attrs):
        if len(attrs['flat_rooms']) < 1:
            raise ValidationError(detail="You should specify at least one room at the flat")
        return attrs
    
    def create(self, validated_data):
        validated_data['room_count'] = len(validated_data['flat_rooms'])
        return super().create(validated_data)



class RentOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RentOrder
        fields = '__all__'
        extra_kwargs = {'renter': {'read_only': True}}

    def create(self, validated_data):
        validated_data['renter'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, attrs):
        if attrs['date_from'] > attrs['date_to'] or attrs['date_from'] < timezone.now().date():
            raise ValidationError(detail="You should specify the correct dates")
        return attrs


class CreateCustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
            required=True,
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
            )
    status = serializers.ChoiceField(CustomUser.USER_STATUS_CHOICES)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'phone', 'birthday', 'age', 'language', 'status')
        extra_kwargs = {'password': {'write_only': True}, 'status': {'required': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            status=validated_data['status']
        )
        
        user.set_password(validated_data['password'])
        user.save()

        return user
