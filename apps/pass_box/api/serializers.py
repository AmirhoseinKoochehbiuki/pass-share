from django.contrib.auth import get_user_model
from rest_framework import serializers
from pass_box.models import *


User = get_user_model()


class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class PassSerializer(serializers.ModelSerializer):
    owner = SimpleUserSerializer(read_only=True)

    class Meta:
        model = PassBox
        fields = [
            'id',
            'owner',
            'pass_code',
            'target'
        ]
        read_only_fields = [
            'id',
            'owner',
        ]

    def create(self, validated_data):
        owner = self.context['request'].user
        return PassBox.objects.create(owner=owner, **validated_data)


class ShareSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShareList
        fields = '__all__'
        read_only_fields = [
            'id'
        ]


class ShareListSerializer(serializers.ModelSerializer):
    pass_code = PassSerializer()
    user = SimpleUserSerializer()

    class Meta:
        model = ShareList
        fields = '__all__'
