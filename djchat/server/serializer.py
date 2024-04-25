from rest_framework import serializers
from .models import Server, Channel, Category


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'


class ServerSerializer(serializers.ModelSerializer):
    num_members = serializers.SerializerMethodField(read_only=True)
    channel_server = ChannelSerializer(many=True, read_only=True)

    class Meta:
        model = Server
        # fields = '__all__'
        exclude = ['member']

    def get_num_members(self, obj):
        if hasattr(obj, 'num_members'):
            return obj.num_members
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        num_members = self.context.get('num_members')
        if not num_members:
            data.pop('num_members', None)
        return data

# class  CategorySerializer(serializers.ModelSerializer):
#     channels=ChannelSerializer(many=True)
#     class Meta:
#         model=Category
#         fields='__all__'

# To many relationship  - one category can have multiple channels but a channel belongs to only one category
